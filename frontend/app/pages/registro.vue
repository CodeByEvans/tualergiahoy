<script setup lang="ts">
import Logo from "~/components/atoms/Logo.vue";
import AlergiasStep from "~/components/organisms/AlergiasStep.vue";
import RegistrationLoading from "~/components/organisms/RegistrationLoading.vue";
import RegistrationStep from "~/components/organisms/RegistrationStep.vue";
import RegistrationSuccess from "~/components/organisms/RegistrationSuccess.vue";
import RegistrationFormTemplate from "~/components/templates/RegistrationFormTemplate.vue";
import { STEPS_CONFIG } from "~/constants/registro";

useHead({
  title: "Registro | tualergiahoy",
  meta: [
    {
      name: "description",
      content:
        "Crea tu perfil y obtén tu informe de polen personalizado con IA.",
    },
  ],
});

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
    class="min-h-screen bg-slate-50 flex flex-col items-center justify-center px-4 py-12"
  >
    <!-- Logo -->
    <NuxtLink to="/">
      <Logo class="w-auto h-16" />
    </NuxtLink>

    <Transition name="fade" mode="out-in">
      <!-- Loader -->
      <div v-if="isSubmitting && !isSuccess" class="w-full max-w-lg">
        <RegistrationLoading
          :progress="serverProgress"
          :message="serverMessage"
        />
      </div>

      <!-- Success -->
      <div v-else-if="isSuccess" class="w-full max-w-lg">
        <RegistrationSuccess :nombre="form.nombre" :email="form.email" />
      </div>

      <!-- Form -->
      <RegistrationFormTemplate
        v-else
        :current-step="pasoActual"
        :total-steps="totalPasos"
        :handle-form-action="handleFormAction"
        :is-submitting="isSubmitting"
        @next="siguientePaso"
        @prev="pasoAnterior"
      >
        <Transition name="fade" mode="out-in">
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
        </Transition>
      </RegistrationFormTemplate>
    </Transition>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
