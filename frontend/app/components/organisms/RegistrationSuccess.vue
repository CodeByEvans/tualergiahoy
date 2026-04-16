<script setup lang="ts">
interface Props {
  nombre: string;
  email: string;
}

defineProps<Props>();

const emit = defineEmits(["finish"]);

const handleGoHome = () => {
  // Emitimos un evento por si la página necesita limpiar algo antes de irse
  emit("finish");
  navigateTo("/");
};
</script>

<template>
  <div class="w-full max-w-lg">
    <UCard
      class="shadow-2xl rounded-[2.5rem] overflow-hidden border-none text-center"
      :ui="{ body: 'p-10' }"
    >
      <div class="mb-8 flex justify-center">
        <div
          class="rounded-full bg-emerald-100 p-5 animate-bounce shadow-inner"
        >
          <UIcon
            name="i-heroicons-check-badge-20-solid"
            class="w-16 h-16 text-emerald-500"
          />
        </div>
      </div>

      <h2 class="text-3xl font-black text-slate-900 mb-3 tracking-tight">
        ¡Todo listo, {{ nombre }}!
      </h2>
      <p class="text-lg text-slate-500 mb-10 leading-relaxed">
        Tu perfil ha sido creado con éxito y nuestra IA ya ha terminado de
        analizar tu caso.
      </p>

      <div
        class="bg-emerald-50/50 border border-emerald-100 rounded-3xl p-6 mb-10 flex items-start gap-4 text-left transition-all hover:bg-emerald-50"
      >
        <div class="p-2 bg-white rounded-xl shadow-sm">
          <UIcon
            name="i-heroicons-envelope-open"
            class="w-6 h-6 text-emerald-600 shrink-0"
          />
        </div>
        <div>
          <p class="text-sm font-bold text-emerald-900">
            Revisa tu bandeja de entrada
          </p>
          <p class="text-sm text-emerald-700/80 leading-snug mt-1">
            Hemos enviado tu <strong>Informe de Previsión</strong> en PDF a
            <span class="font-bold underline decoration-emerald-300">{{
              email
            }}</span
            >.
          </p>
        </div>
      </div>

      <div class="flex flex-col gap-4">
        <UButton
          size="xl"
          block
          color="success"
          class="rounded-2xl font-bold py-4 transition-all hover:scale-[1.02] shadow-lg shadow-emerald-500/20"
          @click="handleGoHome"
        >
          Volver al Inicio
        </UButton>

        <p class="text-xs text-slate-400 font-medium">
          ¿No recibiste el correo? Revisa tu carpeta de spam.
        </p>
      </div>
    </UCard>
  </div>
</template>
