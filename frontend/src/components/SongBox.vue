<script setup>
</script>

<script>
  import axios from "axios";

  export default {
    name: "SongBox",
    props: ['song'],
    methods: {
      async getImage() {
        const response = await axios.get(
            this.$hostname + "img?id=" + this.song.pk,
            { responseType: "blob" }
        );
        this.image = URL.createObjectURL(response.data);
      },
    },
    watch: {
      async song(newSong) {
        this.image = undefined
        const response = await axios.get(
            this.$hostname + "img?id=" + newSong.pk,
            {responseType: "blob"}
        );
        this.image = URL.createObjectURL(response.data);
      }
    },
    created() {
      this.getImage();
    },
    data() {
      return {
        image: undefined
      }
    }
  }
</script>

<template>
  <div v-if="song" class="flex flex-wrap w-full">
    <div class="relative w-full">
      <div class="relative overflow-hidden bg-cover bg-no-repeat aspect-square scale-100 hover:scale-105 ease-in duration-150" style="background-position: 50%">
        <img class="block w-full h-full rounded-lg object-cover object-center" :src="image"/>
        <div class="absolute rounded-lg bottom-0 right-0 left-0 top-0 h-full w-full bg-black bg-fixed opacity-50 overflow-hidden"></div>
        <div class="absolute bottom-5 text-center text-white md:block w-full">
          <p class="text-xl">{{ song.fields.song_name }}</p>
          <p class="text-base">{{ song.fields.song_artist }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>