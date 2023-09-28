<script setup>
import RecordsRack from "@/components/RecordsRack.vue";
import SearchBox from "@/components/SearchBox.vue";
import UpdateButton from "@/components/UpdateButton.vue";
import NoResultsMessage from "@/components/NoResultsMessage.vue";
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
      },
      async addSongs() {
        this.page++;
        const url = this.$hostname + "songs?search=" + encodeURIComponent(this.query) + "&page=" + this.page
        const response = await axios.get(url);
        this.songs = this.songs.concat(response.data)
        this.buttonEnabled = response.data.length === 12;
      }
    },
    data() {
      return {
        songs: undefined,
        query: undefined,
        page: 1,
        buttonEnabled: false
      }
    },
  }
</script>

<template>
  <div class="w-full justify-center flex-row flex pt-6 -mb-2">
    <SearchBox @newSongs="updateSongs"/>
  </div>
  <RecordsRack v-if="songs && songs.length !== 0" :displayed-songs="songs"/>
  <NoResultsMessage v-else-if="songs && query !== ''"/>
  <div v-if="buttonEnabled" class="flex w-full justify-center">
    <UpdateButton @click="addSongs"/>
  </div>
</template>

<style scoped>

</style>
