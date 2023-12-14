<script setup lang="ts">
import { toRefs } from "vue";
import { useQuery } from "vue-query";
import axios from "axios";
import tapeImage from '../assets/tape4.jpg';

const backendURL = import.meta.env.VITE_HOSTNAME;

const props = defineProps({
  song: Object,
});

const { song } = toRefs(props);

const { data: imgUrl, isLoading } = useQuery(['songBoxImage', song.value.pk], async () => {
  const imgApi = new URL('img', backendURL);
  imgApi.searchParams.append('id', song.value.pk);
  const {data} = await axios.get<Blob>(imgApi.toString(), { responseType: 'blob' });
  return URL.createObjectURL(data);
});
</script>

<template>
  <div v-if="song" class="flex flex-wrap w-full">
    <div class="relative w-full">
      <div class="relative overflow-hidden bg-cover bg-no-repeat aspect-square scale-100 hover:scale-105 ease-in duration-150" style="background-position: 50%">
        <img :alt="`Cover of ${song.fields.song_name}`" class="block w-full h-full rounded-lg object-cover object-center" :src="imgUrl || tapeImage"/>
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
