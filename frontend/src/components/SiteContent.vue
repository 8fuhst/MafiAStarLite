<script setup>
import RecordsRack from "@/components/RecordsRack.vue";
import SearchBox from "@/components/SearchBox.vue";
import UpdateButton from "@/components/UpdateButton.vue";
import NoResultsMessage from "@/components/NoResultsMessage.vue";
import DefaultNavbar from "@/components/DefaultNavbar.vue";
</script>

<script>
  import axios from "axios";

  export default {
    methods: {
      async updateSongs(query) {
        this.page = 1;
        const url = this.$hostname + "songs?search=" + encodeURIComponent(query) + "&page=" + this.page
        const response = await axios.get(url);
        this.songs = response.data;
        this.query = query;
        this.buttonEnabled = response.data.length === 12;
        this.displayLatest = false;
      },
      async addSongs() {
        this.page++;
        const url = this.$hostname + "songs?search=" + encodeURIComponent(this.query) + "&page=" + this.page
        const response = await axios.get(url);
        this.songs = this.songs.concat(response.data)
        this.buttonEnabled = response.data.length === 12;
      },
      async randomSong() {
        const url = this.$hostname + "random"
        const response = await axios.get(url)
        this.songs = response.data;
        this.displayLatest = false;
      },
      async latestSongs() {
        const url = this.$hostname + "latest"
        const response = await axios.get(url)
        this.songs = response.data;
        this.displayLatest = true;
        this.buttonEnabled = false;
      }
    },
    created() {
      this.latestSongs();
    },
    data() {
      return {
        songs: undefined,
        query: undefined,
        page: 1,
        buttonEnabled: false,
        displayLatest: true,
      }
    },
  }
</script>

<template>
  <DefaultNavbar @newRandomSong="randomSong"/>
  <div class="grow">
    <div class="w-full justify-center flex-row flex pt-6 -mb-2">
      <SearchBox @newSongs="updateSongs" @empty="latestSongs"/>
    </div>
    <div class="mt-8" v-if="displayLatest">
      <p class="text-3xl">New Tracks</p>
      <RecordsRack :displayed-songs="songs"/>
    </div>
    <RecordsRack v-else-if="songs && songs.length !== 0" :displayed-songs="songs"/>
    <NoResultsMessage v-else-if="songs && query !== ''"/>
    <div v-if="buttonEnabled" class="flex w-full justify-center">
      <UpdateButton @click="addSongs"/>
    </div>
  </div>
</template>

<style scoped>

</style>
