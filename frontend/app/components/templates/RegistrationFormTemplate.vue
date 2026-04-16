<script setup lang="ts">
defineProps<{
  currentStep: number;
  totalSteps: number;
  handleFormAction: () => void;
  isSubmitting?: boolean;
}>();

defineEmits(["next", "prev"]);
</script>

<template>
  <div class="max-w-lg w-full mx-auto px-4">
    <div class="mb-8">
      <div class="flex justify-between text-sm text-slate-500 mb-2">
        <span class="font-bold"
          >Paso {{ currentStep }} de {{ totalSteps }}</span
        >
      </div>
      <div class="w-full bg-slate-200 rounded-full h-2">
        <div
          class="bg-emerald-500 h-2 rounded-full transition-all duration-500"
          :style="{ width: `${(currentStep / totalSteps) * 100}%` }"
        ></div>
      </div>
    </div>

    <form @submit.prevent="handleFormAction">
      <div
        class="bg-white p-8 rounded-3xl border border-slate-200 shadow-sm min-h-[450px]"
      >
        <slot />
        <div class="mt-8">
          <slot name="actions">
            <div class="flex">
              <UButton
                v-if="currentStep > 1"
                type="button"
                color="neutral"
                variant="ghost"
                @click="$emit('prev')"
              >
                <UIcon name="material-symbols:arrow-back-ios" class="w-5 h-5" />
                <span>Atrás</span>
              </UButton>

              <UButton
                class="ml-auto"
                type="submit"
                color="success"
                :loading="isSubmitting"
                :disabled="isSubmitting"
              >
                <span>{{
                  currentStep < totalSteps
                    ? "Siguiente"
                    : isSubmitting
                      ? "Registrando..."
                      : "Registrarme"
                }}</span>
                <UIcon
                  v-if="currentStep < totalSteps"
                  name="material-symbols:arrow-forward-ios"
                  class="w-5 h-5"
                />
              </UButton>
            </div>
          </slot>
        </div>
      </div>
    </form>
  </div>
</template>
