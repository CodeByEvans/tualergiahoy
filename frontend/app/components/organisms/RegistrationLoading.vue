<script setup lang="ts">
import { PASOS_CARGA_IA } from "~/constants/registro";

defineProps<{
  progress: number;
  message: string;
}>();
</script>

<template>
  <UCard class="w-full max-w-lg shadow-xl rounded-3xl" :ui="{ body: 'p-8' }">
    <div class="text-center mb-8">
      <h2 class="text-2xl font-bold text-slate-900">Procesando tu alta</h2>
      <p class="text-slate-500">Estamos preparando todo para ti...</p>
    </div>

    <div class="space-y-6">
      <div
        v-for="step in PASOS_CARGA_IA"
        :key="step.id"
        class="flex items-center gap-4"
      >
        <div
          class="flex-shrink-0 w-8 h-8 flex items-center justify-center rounded-full border-2 transition-all duration-500"
          :class="{
            'border-emerald-500 bg-emerald-50': progress >= step.nextProgress,
            'border-emerald-500 bg-white':
              progress >= step.minProgress && progress < step.nextProgress,
            'border-slate-200 bg-white': progress < step.minProgress,
          }"
        >
          <UIcon
            v-if="progress >= step.nextProgress"
            name="i-heroicons-check-circle-20-solid"
            class="w-6 h-6 text-emerald-500"
          />
          <UIcon
            v-else-if="progress >= step.minProgress"
            name="i-heroicons-arrow-path-20-solid"
            class="w-5 h-5 text-emerald-500 animate-spin"
          />
          <div v-else class="w-2 h-2 bg-slate-300 rounded-full"></div>
        </div>

        <div class="flex-grow">
          <p
            class="text-sm font-semibold transition-colors duration-300"
            :class="
              progress >= step.minProgress ? 'text-slate-900' : 'text-slate-400'
            "
          >
            {{ step.label }}
          </p>
          <p
            v-if="progress >= step.minProgress && progress < step.nextProgress"
            class="text-xs text-emerald-600 animate-pulse"
          >
            {{ message }}
          </p>
        </div>
      </div>
    </div>

    <div class="mt-10">
      <div
        class="flex justify-between text-xs font-bold text-slate-400 mb-2 uppercase tracking-wider"
      >
        <span>Progreso general</span>
        <span>{{ progress }}%</span>
      </div>
      <div class="w-full bg-slate-100 rounded-full h-3 overflow-hidden">
        <div
          class="bg-emerald-500 h-full transition-all duration-700 ease-out"
          :style="{ width: `${progress}%` }"
        ></div>
      </div>
    </div>
  </UCard>
</template>
