<script setup lang="ts">
import { ALERGENOS, SEVERIDADES } from "~/constants/alergias";
import type { RegistroForm } from "~/types/RegisterForm";

defineProps<{
  form: RegistroForm;
  errors: Record<string, string>;
}>();

const emit = defineEmits(["toggleAlergia", "setSeveridad"]);
</script>

<template>
  <div class="flex flex-col gap-6">
    <header>
      <h2 class="text-2xl font-bold text-slate-900 mb-1">Salud y Alergias</h2>
      <p class="text-slate-500">Selecciona tus alergias y su intensidad</p>
    </header>

    <div class="flex flex-col gap-6">
      <UFormField label="Alergias conocidas" required :error="errors.alergias">
        <div class="flex flex-wrap gap-2 mt-1">
          <button
            v-for="alergia in ALERGENOS"
            :key="alergia"
            type="button"
            class="px-4 py-2 rounded-full text-sm font-medium border transition-all duration-200"
            :class="
              form.alergias.find((a) => a.nombre === alergia)
                ? 'bg-emerald-500 text-white border-emerald-500'
                : 'bg-white text-slate-600 border-slate-200 hover:border-emerald-400'
            "
            @click="$emit('toggleAlergia', alergia)"
          >
            {{ alergia }}
          </button>
        </div>
      </UFormField>

      <Transition name="fade-down">
        <div v-if="form.alergias.length > 0" class="flex flex-col gap-4">
          <p class="text-sm font-semibold text-slate-700">
            Severidad por alergia
          </p>

          <TransitionGroup name="alergia" tag="div" class="flex flex-col gap-3">
            <div
              v-for="alergia in form.alergias"
              :key="alergia.nombre"
              class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between p-4 bg-slate-50 rounded-2xl border border-slate-200"
            >
              <span class="text-sm font-semibold text-slate-800">
                {{ alergia.nombre }}
              </span>

              <div class="flex gap-2 flex-wrap">
                <button
                  v-for="severidad in SEVERIDADES"
                  :key="severidad.value"
                  type="button"
                  class="px-4 py-2 rounded-full text-sm font-medium border transition-all duration-200"
                  :class="
                    alergia.severidad === severidad.value
                      ? 'bg-emerald-500 text-white border-emerald-500'
                      : 'bg-white text-slate-600 border-slate-200 hover:border-emerald-400'
                  "
                  @click="
                    $emit('setSeveridad', alergia.nombre, severidad.value)
                  "
                >
                  {{ severidad.label }}
                </button>
              </div>
            </div>
          </TransitionGroup>
        </div>
      </Transition>

      <UFormField label="Medicación Actual" :error="errors.medicacion">
        <UInput
          v-model="form.medicacion"
          placeholder="Ej: Loratadina 10mg (Opcional)"
          class="w-full"
        />
      </UFormField>
    </div>
  </div>
</template>

<style scoped>
/* Las transiciones que hacen que se vea fluido */
.fade-down-enter-active,
.fade-down-leave-active {
  transition: all 0.5s ease-out;
}
.fade-down-enter-from,
.fade-down-leave-to {
  opacity: 0;

  transform: scale(0.95);
}

.alergia-enter-active,
.alergia-leave-active {
  transition: all 0.3s ease;
}
.alergia-enter-from,
.alergia-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
</style>
