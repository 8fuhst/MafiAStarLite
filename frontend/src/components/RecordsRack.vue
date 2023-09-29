<script setup>
</script>

<script>
import SongBox from "./SongBox.vue";

export default {
  name: "RecordsRack",
  props: ['displayedSongs'],
  components: {
    SongBox
  },
  data() {
    return {
      songs: ['']
    }
  },
}
</script>

<template>
  <div class="songs_container mx-auto px-5 py-2 lg:px-32 lg:pt-12 max-w-screen-xl">
    <div class="songs_content align-middle grid grid-cols-2 lg:grid-cols-3 gap-7 justify-evenly">
        <songBox v-for="song in displayedSongs" :key="song.song_id" :song=song></songBox>
    </div>
  </div>
</template>

<style scoped>

</style>
