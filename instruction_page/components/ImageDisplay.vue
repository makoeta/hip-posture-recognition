<script lang="ts" setup>
const props = defineProps<{ imageUrls: string[] }>();

const getClearImUrl = (imgUrl: string) => {
  let url = useRuntimeConfig().app.baseURL + imgUrl;
  if (url.startsWith("/")) {
    url = url.substring(1, url.length);
  }
  return url;
};
</script>

<template>
  <div class="w-full px-[3%]">
    <div class="carousel w-full">
      <div
        v-for="(imgUrl, index) in props.imageUrls"
        :id="'slide' + index"
        :key="imgUrl"
        class="carousel-item relative w-full"
      >
        <img
          :alt="getClearImUrl(imgUrl)"
          :src="getClearImUrl(imgUrl)"
          class="w-full"
        />

        <div
          class="absolute top-1/2 right-5 left-5 flex -translate-y-1/2 justify-between"
        />
        <div
          v-if="imageUrls.length > 1"
          class="absolute top-1/2 right-5 left-5 flex -translate-y-1/2 justify-between"
        >
          <a
            :href="
              '#slide' +
              (index - 1 >= 0 ? index - 1 : props.imageUrls.length - 1)
            "
            class="btn btn-circle"
          >
            ❮
          </a>

          <a
            :href="
              '#slide' + (index + 1 < props.imageUrls.length ? index + 1 : 0)
            "
            class="btn btn-circle"
          >
            ❯
          </a>
        </div>
      </div>
    </div>
  </div>
</template>
