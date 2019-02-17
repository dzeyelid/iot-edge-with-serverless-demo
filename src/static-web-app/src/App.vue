<template>
  <div id="app" class="container">
    <Status/>
  </div>
</template>

<script lang="ts">
import 'bulma';
import { Component, Vue } from 'vue-property-decorator';
import Status from './components/Status.vue';

@Component({
  components: {
    Status,
  },
})
export default class App extends Vue {}
</script>

<style>
</style>
