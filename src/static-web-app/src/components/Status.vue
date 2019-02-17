<template>
  <div class="tile is-ancestor">
    <div class="tile is-vertical">
      <div class="tile is-parent is-vertical">
        <div class="tile is-child">
          <div class="field">
            <label for="apiBaseUrl" class="label">API endpint URI</label>
            <div class="control">
              <input v-model="apiBaseUrl" v-bind:disabled="ready" type="text" class="input" placeholder="Input API endpint URI here">
            </div>
          </div>
          <div class="field is-grouped">
            <div class="control">
              <button v-on:click="connectToSignalR" v-bind:disabled="ready" class="button is-link">Connect</button>
            </div>
            <div class="control">
              <button class="button" v-on:click="cancelConnection">cancel</button>
            </div>
          </div>
        </div>
        <div v-if="ready" class="title is-child">
          <pre v-if="!status" class="is-family-code">Waiting..</pre>
          <pre v-else class="is-family-code">{{ status }}</pre>
        </div>
      </div>
    </div>

    <ErrorModal v-model="errorMessage" v-on:close="purgeErrorMessage()" />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import axios, { AxiosInstance, AxiosResponse } from 'axios';
import { HubConnectionBuilder, HubConnection, IHttpConnectionOptions } from '@aspnet/signalr';
import ErrorModal from './ErrorModal.vue';

@Component({
  components: {
    ErrorModal,
  },
})
export default class Status extends Vue {
  private status: string = '';
  private ready: boolean = false;
  private apiBaseUrl: string = 'http://localhost:7071';
  private errorMessage: string|null = null;

  private httpClient: AxiosInstance|null = null;
  private connection: HubConnection|null = null;

  private async connectToSignalR(): Promise<void> {
    try {
      const connection = await this.getConnection();

      connection.on('newMessage', (message) => {
        this.$data.status = message;
      });

      await connection.start();
      this.$data.ready = true;
    } catch (error) {
      this.purgeHttpClient();
      this.showErrorMessage(error);
    }
  }

  private cancelConnection(): void {
    this.purgeConnection();
    this.purgeHttpClient();
    this.$data.status = '';
    this.$data.ready = false;
  }

  private async getConnection(): Promise<HubConnection> {
    if (this.connection == null) {
      const httpClient = await this.getHttpCient();
      const result: AxiosResponse<any> = await httpClient.post(
        '/api/negotiate',
      );

      const { data } = result;
      const { accessToken, url } = data;

      if (accessToken == null || url == null) {
        throw new Error('Failed to get the token or url to access the SignalR Service.');
      }

      const options: IHttpConnectionOptions = {
        accessTokenFactory: () => accessToken,
      };

      this.connection = new HubConnectionBuilder()
        .withUrl(url, options)
        .build();
    }

    return this.connection;
  }

  private purgeConnection(): void {
    if (this.connection != null) {
      this.connection.stop();
      delete this.connection;
    }
  }

  private async getHttpCient(): Promise<AxiosInstance> {
    if (this.httpClient == null) {
      this.httpClient = await axios.create({
        baseURL: this.$data.apiBaseUrl,
        headers: {
          common: {
            'Content-Type': 'text/json',
          },
        },
      });
    }
    return this.httpClient;
  }

  private purgeHttpClient(): void {
    delete this.httpClient;
  }

  private showErrorMessage(error: Error): void {
    this.$data.errorMessage = error.toString();
  }

  private purgeErrorMessage(): void {
    this.$data.errorMessage = null;
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
