<script>
import {defineComponent} from 'vue'

export default defineComponent({
  name: "DefaultFooter"
})
</script>

<template>

  <footer class="flex bg-white rounded-lg shadow m-4 dark:bg-gray-800 bottom-0">
    <div class="flex w-full mx-auto max-w-screen-xl p-4 md:flex md:items-center md:justify-between bottom-0">
      <span class="text-sm text-gray-500 sm:text-center dark:text-gray-400">© 2023 <a href="https://noahfuhst.de/" class="hover:underline">Noah Fuhst</a>, All Rights Reserved.
    </span>
    </div>
  </footer>

</template>

<style scoped>

</style>