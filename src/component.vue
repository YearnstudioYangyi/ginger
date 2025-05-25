<template>
  <div class="box">
    <span>{{ 数字 }}</span>
    <span>点击增加</span>
    <button @click="增加(15)">增加十五</button>
    <button @click="增加(10)">增加十</button>
    <button @click="增加(1)">增加一</button>
    <button @click="增加随机数值()">增加随机数值</button>
    <button @click="增加随机浮点数()">增加随机数值2</button>
    <span class="text">Powered by Ginger & Vue3 & Webpack</span>
  </div>
</template>
<script lang="ts" setup>
import { ref } from 'vue';
const 数字 = ref(0);
function 生成随机小数() {
  return Math.random();
}
function 生成随机整数() {
  return Math.floor(Math.random() * 100);
}
function 增加(值: number) {
  数字.value += 值;
}
function 增加随机数值() {
  增加(生成随机整数());
}
function 增加随机浮点数() {
  增加(生成随机小数());
}
</script>
<style scoped>
div.box {
  width: 200px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 5px;
  border: 1px solid grey;
  border-radius: 5px;
}
span.text {
  white-space: nowrap;
}
</style>