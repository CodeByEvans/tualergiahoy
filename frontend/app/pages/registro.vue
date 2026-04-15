<script setup lang="ts">
import AlergiasStep from "~/components/organisms/AlergiasStep.vue";
import RegistrationStep from "~/components/organisms/RegistrationStep.vue";
import RegistrationFormTemplate from "~/components/templates/RegistrationFormTemplate.vue";
import { STEPS_CONFIG } from "~/constants/registro";

definePageMeta({
  layout: false,
});

const {
  isSubmitting,
  serverMessage,
  serverProgress,
  isSuccess,
  form,
  pasoActual,
  totalPasos,
  errors,
  clearError,
  siguientePaso,
  pasoAnterior,
  toggleAlergia,
  setSeveridad,
  submit,
} = useRegistroForm();

const pasosVisuales = [
  { id: 1, label: "Creación de perfil", minProgress: 10, nextProgress: 25 },
  {
    id: 2,
    label: "Geolocalización y entorno",
    minProgress: 25,
    nextProgress: 40,
  },
  {
    id: 3,
    label: "Análisis de niveles de polen",
    minProgress: 40,
    nextProgress: 75,
  },
  {
    id: 4,
    label: "Generación de informe IA",
    minProgress: 75,
    nextProgress: 85,
  },
  {
    id: 5,
    label: "Personalización de documento PDF",
    minProgress: 85,
    nextProgress: 95,
  },
  {
    id: 6,
    label: "Envío de documentación por email",
    minProgress: 95,
    nextProgress: 101,
  },
];

watch(
  () => [form.value.password, form.value.password_confirmation],
  () => {
    const pass = form.value.password;
    const confirm = form.value.password_confirmation;

    if (confirm.length < pass.length) {
      clearError("password_confirmation");
      return;
    }

    if (pass !== confirm) {
      errors.value.password_confirmation = "Las contraseñas no coinciden";
      return;
    }

    if (form.value.password_confirmation === form.value.password) {
      clearError("password_confirmation");
    }
  },
);

const handleFormAction = () => {
  if (pasoActual.value < totalPasos) {
    siguientePaso();
  } else {
    submit();
  }
};
</script>

<template>
  <div
    class="min-h-screen bg-slate-50 flex items-center justify-center px-4 py-12"
  >
    <!-- Logo -->
    <div class="absolute top-6 left-8">
      <NuxtLink to="/">
        <img src="~/assets/logo.png" alt="Logo" class="w-auto h-16" />
      </NuxtLink>
    </div>

    <div v-if="isSubmitting && !isSuccess" class="w-full max-w-lg">
      <UCard class="shadow-xl rounded-3xl" :ui="{ body: 'p-8' }">
        <div class="text-center mb-8">
          <h2 class="text-2xl font-bold text-slate-900">Procesando tu alta</h2>
          <p class="text-slate-500">Estamos preparando todo para ti...</p>
        </div>

        <div class="space-y-6">
          <div
            v-for="step in pasosVisuales"
            :key="step.id"
            class="flex items-center gap-4"
          >
            <div
              class="flex-shrink-0 w-8 h-8 flex items-center justify-center rounded-full border-2 transition-all duration-500"
              :class="[
                serverProgress >= step.nextProgress
                  ? 'border-emerald-500 bg-emerald-50'
                  : serverProgress >= step.minProgress
                    ? 'border-emerald-500 bg-white'
                    : 'border-slate-200 bg-white',
              ]"
            >
              <UIcon
                v-if="serverProgress > step.nextProgress"
                name="i-heroicons-check-circle-20-solid"
                class="w-6 h-6 text-emerald-500"
              />
              <UIcon
                v-else-if="serverProgress >= step.minProgress"
                name="i-heroicons-arrow-path-20-solid"
                class="w-5 h-5 text-emerald-500 animate-spin"
              />
              <div v-else class="w-2 h-2 bg-slate-300 rounded-full"></div>
            </div>

            <div class="flex-grow">
              <p
                class="text-sm font-semibold transition-colors duration-300"
                :class="
                  serverProgress >= step.minProgress
                    ? 'text-slate-900'
                    : 'text-slate-400'
                "
              >
                {{ step.label }}
              </p>
              <p
                v-if="
                  serverProgress >= step.minProgress &&
                  serverProgress < step.nextProgress
                "
                class="text-xs text-emerald-600 animate-pulse"
              >
                {{ serverMessage }}
              </p>
            </div>
          </div>
        </div>

        <div class="mt-10">
          <div
            class="flex justify-between text-xs font-bold text-slate-400 mb-2 uppercase tracking-wider"
          >
            <span>Progreso general</span>
            <span>{{ serverProgress }}%</span>
          </div>
          <div class="w-full bg-slate-100 rounded-full h-3 overflow-hidden">
            <div
              class="bg-emerald-500 h-full transition-all duration-700 ease-out"
              :style="{ width: `${serverProgress}%` }"
            ></div>
          </div>
        </div>
      </UCard>
    </div>

    <div v-else-if="isSuccess" class="w-full max-w-lg">
      <UCard
        class="shadow-2xl rounded-3xl overflow-hidden border-none text-center"
        :ui="{ body: 'p-10' }"
      >
        <div class="mb-6 flex justify-center">
          <div class="rounded-full bg-emerald-100 p-4 animate-bounce">
            <UIcon
              name="i-heroicons-check-badge-20-solid"
              class="w-16 h-16 text-emerald-500"
            />
          </div>
        </div>

        <h2 class="text-3xl font-extrabold text-slate-900 mb-2">
          ¡Todo listo, {{ form.nombre }}!
        </h2>
        <p class="text-lg text-slate-600 mb-8">
          Tu perfil ha sido creado con éxito y nuestra IA ya ha terminado de
          analizar tu caso.
        </p>

        <div
          class="bg-emerald-50 border border-emerald-100 rounded-2xl p-6 mb-8 flex items-start gap-4 text-left"
        >
          <UIcon
            name="i-heroicons-envelope-open"
            class="w-6 h-6 text-emerald-600 shrink-0 mt-1"
          />
          <div>
            <p class="text-sm font-bold text-emerald-900">
              Revisa tu bandeja de entrada
            </p>
            <p class="text-sm text-emerald-700/80">
              Hemos enviado tu <strong>Informe de Previsión de Polen</strong> en
              PDF a <span class="underline">{{ form.email }}</span
              >.
            </p>
          </div>
        </div>

        <div class="flex flex-col gap-3">
          <UButton
            size="xl"
            block
            variant="solid"
            class="rounded-xl font-bold transition-transform hover:scale-[1.02]"
            @click="navigateTo('/')"
          >
            Ir al Inicio
          </UButton>

          <p class="text-xs text-slate-400">
            ¿No recibiste el correo? Revisa tu carpeta de spam.
          </p>
        </div>
      </UCard>
    </div>

    <RegistrationFormTemplate
      v-else
      :current-step="pasoActual"
      :total-steps="totalPasos"
      :handle-form-action="handleFormAction"
      :is-submitting="isSubmitting"
      @next="siguientePaso"
      @prev="pasoAnterior"
    >
      <RegistrationStep
        v-if="pasoActual === 1"
        v-bind="STEPS_CONFIG.PERSONAL"
        :form="form"
        :errors="errors"
        :clear-error="clearError"
      />

      <AlergiasStep
        v-else-if="pasoActual === 2"
        :form="form"
        :errors="errors"
        @toggle-alergia="toggleAlergia"
        @set-severidad="setSeveridad"
      />

      <RegistrationStep
        v-else-if="pasoActual === 3"
        v-bind="STEPS_CONFIG.ACCOUNT"
        :form="form"
        :errors="errors"
        :clear-error="clearError"
      />
    </RegistrationFormTemplate>
  </div>
</template>
