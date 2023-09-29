<script setup>
import { Disclosure } from '@headlessui/vue'
</script>

<script>
export default {
  name: "DefaultNavbar",
}
</script>

<template>
  <Disclosure as="nav" class="bg-gray-800">
    <div class="mx-auto max-w-7xl px-2 sm:px-6 lg:px-8">
      <div class="relative flex h-16 items-center justify-between">
        <div class="flex flex-1 items-center justify-center sm:items-stretch sm:justify-start">
          <div class="flex flex-shrink-0 items-center">
            <img class="hidden h-8 mb-1 w-auto lg:block" src="../assets/ultrastar_bit.svg" alt="Ultrastar Bit" />
          </div>
          <div class="align-middle pl-2">
            <h4 class="align-middle mt-1 text-xl text-white">MafiAStarLite</h4>
          </div>
        </div>
      </div>
    </div>
  </Disclosure>
</template>

<style scoped>

</style>
