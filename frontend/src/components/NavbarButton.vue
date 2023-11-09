<script>
import {defineComponent} from 'vue'

export default defineComponent({
  name: "NavbarButton",
  props: ['text']
})
</script>

<template>
  <button class="bg-transparent border border-indigo-800 rounded px-3 py-0.5 hover:bg-indigo-800
  text-gray-200 transition-colors font-light hover:shadow-inner">{{ text }}</button>
</template>

<style scoped>

</style>