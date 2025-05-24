<template>
  <div class="box">
    <span>{{数字}}</span>
    <br/>
    <button @click="增加">增加</button>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue';

const 数字 = ref(0);

function 增加() {
  数字.value += 1;
}
</script>

<style scoped>
  .box {
    width: 200px;
    height: 100px;
    display: flex;
    justify-content: center;
    align-items: center;
    border: 1px solid gray;
    border-radius: 5px;
    flex-direction: column;
  }
</style>