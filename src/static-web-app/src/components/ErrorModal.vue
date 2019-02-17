<template>
  <div class="modal" id="errorModal" v-bind:class="{ 'is-active': isActive() }">
    <div class="modal-background"></div>
    <div class="modal-content notification">
      Error occured...
      <pre class="is-family-code">{{ JSON.stringify(errorMessage, null, 2) }}</pre>
    </div>
    <button class="modal-close is-large" aria-label="close" v-on:click="close"></button>
  </div>
</template>

<script lang="ts">
import { Component, Model, Watch, Emit, Vue } from 'vue-property-decorator';

@Component
export default class ErrorModal extends Vue {
  @Model('change', { type: String }) private errorMessage: string|null = null;
  @Watch('errorMessage', { immediate: true, deep: true})
  private onErrorMessageChanged(val: string, oldVal: string): void {
    this.$data.errorMessage = val;
  }
  @Emit()
  private close(): void {
    this.$data.errorMessage = null;
  }

  private isActive(): boolean {
    return this.$data.errorMessage != null;
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
