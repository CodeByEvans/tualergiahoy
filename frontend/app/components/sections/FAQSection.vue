<script setup lang="ts">
const items = [
  {
    label: "¿Es gratuito?",
    content:
      "Sí, el registro y el primer informe son completamente gratuitos. Queremos que pruebes el valor del servicio sin compromisos. Sin tarjetas de crédito.",
    icon: "i-heroicons-banknotes",
  },
  {
    label: "¿Con qué frecuencia recibiré mi informe?",
    content:
      "Recibirás tu informe personalizado cada lunes por la mañana directamente en tu bandeja de entrada, preparado para tu semana.",
    icon: "i-heroicons-calendar-days",
  },
  {
    label: "¿Qué datos necesito para registrarme?",
    content:
      "Solo nombre, ciudad y tus alergias. El proceso es ultra rápido, diseñado para completarse en menos de 2 minutos.",
    icon: "i-heroicons-user-plus",
  },
  {
    label: "¿Cómo obtenéis los datos de polen?",
    content:
      "Nos conectamos con la API de Open-Meteo y el modelo CAMS Europeo, garantizando datos científicos actualizados en tiempo real.",
    icon: "i-heroicons-beaker",
  },
  {
    label: "¿Quién genera el pronóstico de salud?",
    content:
      "Nuestra IA propietaria analiza tu perfil clínico frente a las condiciones ambientales para redactar consejos específicos para ti.",
    icon: "i-heroicons-cpu-chip",
  },
  {
    label: "¿Puedo cambiar mis alergias después?",
    content:
      "¡Por supuesto! Estamos habilitando el área personal. Mientras tanto, escríbenos a hola@tualergiahoy.com y lo gestionamos por ti.",
    icon: "i-heroicons-pencil-square",
  },
];
</script>

<template>
  <section class="faq-section">
    <div class="max-w-4xl mx-auto px-6">
      <div class="text-center mb-16">
        <UBadge
          color="success"
          variant="subtle"
          label="Centro de ayuda"
          class="rounded-full px-4 mb-4"
        />
        <h2
          class="text-4xl md:text-5xl font-black text-slate-900 tracking-tight"
        >
          Preguntas <span class="text-emerald-600">frecuentes</span>
        </h2>
        <p class="mt-5 text-lg text-slate-500">
          Todo lo que necesitas saber antes de empezar a respirar mejor.
        </p>
      </div>

      <div class="faq-container">
        <ClientOnly>
          <UAccordion :items="items" multiple>
            <template #default="{ item, open }">
              <UButton
                color="neutral"
                variant="ghost"
                class="w-full flex justify-between items-center text-left py-5 px-6"
                :class="[
                  open ? 'text-emerald-700 bg-emerald-50/30' : 'text-slate-900',
                ]"
              >
                <span class="text-lg font-bold tracking-tight">{{
                  item.label
                }}</span>
                <template #trailing>
                  <UIcon
                    :name="open ? 'i-heroicons-minus' : 'i-heroicons-plus'"
                    class="w-5 h-5 transition-transform duration-200"
                    :class="[open ? 'text-emerald-600' : 'text-slate-400']"
                  />
                </template>
              </UButton>
            </template>

            <template #body="{ item }">
              <div
                class="px-6 pb-6 pt-2 text-slate-500 text-lg leading-relaxed"
              >
                {{ item.content }}
              </div>
            </template>
          </UAccordion>
        </ClientOnly>
      </div>

      <div
        class="mt-16 text-center bg-slate-900 rounded-3xl p-10 relative overflow-hidden"
      >
        <div
          class="absolute top-0 right-0 w-32 h-32 bg-emerald-500/10 rounded-full -translate-y-1/2 translate-x-1/2 blur-3xl"
        ></div>

        <h3 class="text-white text-2xl font-bold mb-2">¿Aún tienes dudas?</h3>
        <p class="text-slate-400 mb-6">
          Estamos aquí para ayudarte a sentirte mejor.
        </p>
        <UButton
          to="mailto:hola@tualergiahoy.com"
          color="success"
          size="xl"
          class="rounded-xl px-8 font-bold"
        >
          Contactar con soporte
        </UButton>
      </div>
    </div>
  </section>
</template>

<style scoped>
.faq-section {
  padding: 120px 0;
  background-color: #ffffff;
}

:deep(.u-accordion) {
  --tw-ring-color: transparent !important;
}
</style>
