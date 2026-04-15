<script setup lang="ts">
const beneficios = [
  {
    icono: "material-symbols:account-circle",
    titulo: "Personalizado para ti",
    descripcion:
      "Analizamos tus alergias específicas y ciudad para que la información sea 100% relevante para tu salud.",
    accent: "bg-emerald-50 text-emerald-600",
  },
  {
    icono: "material-symbols:electric-bolt-rounded",
    titulo: "Datos en tiempo real",
    descripcion:
      "Conexión directa con estaciones meteorológicas. Si el polen sube, tú lo sabrás al instante.",
    accent: "bg-blue-50 text-blue-600",
  },
  {
    icono: "i-heroicons-cpu-chip",
    titulo: "Inteligencia Artificial",
    descripcion:
      "Nuestra IA interpreta los datos complejos y los traduce en consejos prácticos para tu día a día.",
    accent: "bg-indigo-50 text-indigo-600",
  },
  {
    icono: "material-symbols:attach-email",
    titulo: "Directo a tu email",
    descripcion:
      "Recibe un informe semanal en PDF, visual y fácil de leer, sin tener que entrar en ninguna app.",
    accent: "bg-amber-50 text-amber-600",
  },
];
</script>

<template>
  <section class="benefits-section">
    <div class="max-w-6xl mx-auto px-6">
      <div
        class="flex flex-col md:flex-row md:items-end justify-between mb-16 gap-6"
      >
        <div class="max-w-2xl">
          <UBadge
            color="primary"
            variant="subtle"
            label="¿Por qué nosotros?"
            class="rounded-full px-4 mb-4"
          />
          <h2
            class="text-4xl md:text-5xl font-black text-slate-900 tracking-tight"
          >
            Todo lo que necesitas para <br class="hidden md:block" />
            <span class="text-emerald-600">domar tu alergia</span>
          </h2>
        </div>
        <p class="text-lg text-slate-500 max-w-sm">
          Hemos diseñado una herramienta que se adapta a tu vida, y no al revés.
        </p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <UCard
          v-for="(beneficio, index) in beneficios"
          :key="index"
          class="group border-none shadow-sm ring-1 ring-slate-200/60 hover:ring-emerald-500/30 hover:shadow-xl hover:shadow-emerald-500/5 transition-all duration-500 rounded-3xl"
          :ui="{ body: 'p-8' }"
        >
          <div class="flex flex-col sm:flex-row gap-6">
            <div
              :class="[beneficio.accent]"
              class="w-16 h-16 shrink-0 rounded-2xl flex items-center justify-center group-hover:scale-110 transition-transform duration-500 shadow-sm"
            >
              <UIcon :name="beneficio.icono" class="w-8 h-8" />
            </div>

            <div>
              <h3
                class="text-xl font-bold text-slate-900 mb-2 group-hover:text-emerald-600 transition-colors"
              >
                {{ beneficio.titulo }}
              </h3>
              <p class="text-slate-500 leading-relaxed">
                {{ beneficio.descripcion }}
              </p>
            </div>
          </div>
        </UCard>
      </div>
    </div>
  </section>
</template>

<style scoped>
.benefits-section {
  padding: 100px 0;
  background-color: #f8fafc;
  position: relative;
}

.benefits-section::before {
  content: "";
  position: absolute;
  top: 0;
  right: 0;
  width: 400px;
  height: 400px;
  background: radial-gradient(
    circle,
    rgba(16, 185, 129, 0.05) 0%,
    transparent 70%
  );
  z-index: 0;
}

:deep(.u-card) {
  position: relative;
  z-index: 1;
}
</style>
