<template>
  <div class="min-h-screen bg-slate-900 text-white flex flex-col items-center justify-center p-8">
    <h1 class="text-4xl font-bold mb-6">BioChemVerse</h1>
    <p class="mb-8 text-slate-300">Kerangka Anatomi Tubuh Manusia</p>
    <AnatomyBody />
  </div>
</template>

<script setup>
import AnatomyBody from './components/AnatomyBody.vue'
</script>