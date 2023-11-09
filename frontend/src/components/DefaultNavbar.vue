<script setup>
import {Disclosure, DisclosureButton, DisclosurePanel} from '@headlessui/vue'
import { Bars3Icon, XMarkIcon } from '@heroicons/vue/24/outline'
import NavbarButton from "@/components/NavbarButton.vue";
</script>

<script>

export default {
  name: "DefaultNavbar",
  methods: {
    async openSonglist() {
      window.location.href = this.$hostname + "songlist"
    },
    async getRandomData() {
      this.$emit('newRandomSong')
    }
  }
}

</script>

<template>
  <Disclosure as="nav" class="bg-gray-800">
    <div class="mx-auto max-w-7xl px-2 sm:px-6 lg:px-8">
      <div class="relative flex h-16 items-center justify-between">
        <div class="absolute inset-y-0 left-0 flex items-center sm:hidden">
          <!-- Mobile menu button-->
          <DisclosureButton class="inline-flex items-center justify-center rounded-md p-2 text-gray-400 hover:bg-gray-700 hover:text-white focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white">
            <span class="sr-only">Open main menu</span>
            <Bars3Icon v-if="!open" class="block h-6 w-6" aria-hidden="true" />
            <XMarkIcon v-else class="block h-6 w-6" aria-hidden="true" />
          </DisclosureButton>
        </div>
        <div class="flex flex-1 items-center justify-center sm:items-stretch sm:justify-start">
          <div class="flex flex-shrink-0 items-center">
            <img class="hidden h-8 mb-1 w-auto lg:block" src="../assets/ultrastar_bit.svg" alt="Ultrastar Bit" />
          </div>
          <div class="align-middle pl-2">
            <h4 class="align-middle mt-1 text-xl text-white">MafiAStarLite</h4>
          </div>
          <div class="hidden items-center sm:ml-6 sm:block">
            <div class="flex">
              <div class="flex space-x-4 mr-4">
                <NavbarButton @click="openSonglist" text="Songlist"></NavbarButton>
              </div>
              <div class="flex space-x-4 mr-4">
                <NavbarButton @click="getRandomData" text="Random Song"></NavbarButton>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <DisclosurePanel class="sm:hidden">
      <div class="space-y-1 px-2 pb-3 pt-2">
        <button @click="openSonglist" class="text-gray-300 hover:bg-gray-700 hover:text-white">Songliste</button>
      </div>
      <div class="space-y-1 px-2 pb-3 pt-2">
        <button @click="getRandomData" class="text-gray-300 hover:bg-gray-700 hover:text-white">Random Song</button>
      </div>
    </DisclosurePanel>
  </Disclosure>
</template>

<style scoped>

</style>