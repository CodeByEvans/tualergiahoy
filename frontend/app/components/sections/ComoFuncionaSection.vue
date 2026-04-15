<script setup lang="ts">
const pasos = [
  {
    icono: "material-symbols:how-to-reg",
    titulo: "Regístrate",
    descripcion:
      "Crea tu perfil en menos de 2 minutos indicando tus alergias y ubicación habitual.",
  },
  {
    icono: "material-symbols:map-pin-review",
    titulo: "Analizamos tu zona",
    descripcion:
      "Nuestros algoritmos cruzan datos de estaciones de polen locales en tiempo real.",
  },
  {
    icono: "material-symbols:article-person",
    titulo: "Recibes tu informe",
    descripcion:
      "Un pronóstico inteligente y personalizado llega a tu correo cada lunes mañana.",
  },
];
</script>

<template>
  <section class="how-it-works">
    <div class="max-w-6xl mx-auto px-6">
      <div class="text-center mb-20">
        <UBadge
          variant="subtle"
          label="Simplificamos tu vida"
          class="px-4 py-1.5 rounded-full text-xs font-bold uppercase tracking-wider mb-6"
        />
        <h2
          class="text-4xl md:text-5xl font-black text-slate-900 tracking-tight"
        >
          Tres pasos, <span class="text-emerald-600">sin complicaciones</span>
        </h2>
        <p class="mt-5 text-xl text-slate-500 max-w-2xl mx-auto">
          Todo el proceso es automático. Nosotros nos encargamos de los datos,
          tú de respirar tranquilo.
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-10">
        <div v-for="(paso, index) in pasos" :key="index" class="relative group">
          <div
            v-if="index < pasos.length - 1"
            class="hidden md:block absolute top-16 left-full w-full h-[2px] bg-slate-100 -z-10"
          />

          <UCard
            class="h-full border-none shadow-sm ring-1 ring-slate-200/60 hover:ring-emerald-500/30 hover:shadow-xl hover:shadow-emerald-500/5 transition-all duration-500 rounded-3xl overflow-hidden"
            :ui="{
              body: 'p-8',
            }"
          >
            <div
              class="relative w-20 h-20 mx-auto mb-8 flex items-center justify-center rounded-2xl bg-emerald-50 group-hover:scale-110 transition-transform duration-500"
            >
              <UIcon :name="paso.icono" class="w-8 h-8" />
              <div
                class="absolute -top-2 -right-2 w-8 h-8 bg-white border-2 border-emerald-500 text-emerald-600 rounded-full flex items-center justify-center font-bold text-sm shadow-sm"
              >
                {{ index + 1 }}
              </div>
            </div>

            <div class="text-center">
              <h3 class="text-2xl font-bold text-slate-900 mb-4 tracking-tight">
                {{ paso.titulo }}
              </h3>
              <p class="text-slate-500 leading-relaxed text-lg">
                {{ paso.descripcion }}
              </p>
            </div>
          </UCard>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.how-it-works {
  padding: 120px 0;
  background: radial-gradient(circle at 50% -20%, #ecfdf5 0%, #ffffff 50%);
  position: relative;
  overflow: hidden;
}
</style>
