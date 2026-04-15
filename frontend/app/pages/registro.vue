<script setup lang="ts">
import { ALERGENOS, SEVERIDADES } from "~/constants/alergias";
import { CIUDADES } from "~/constants/ciudades";

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
  showPassword,
  showConfirmPassword,
  clearError,
  siguientePaso,
  pasoAnterior,
  toggleAlergia,
  setSeveridad,
  onPhoneInput,
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

const getStatusClass = (minProgress: number) => {
  if (
    serverProgress.value >=
    pasosVisuales.find((p) => p.minProgress === minProgress)!.nextProgress
  ) {
    return "border-emerald-500 bg-emerald-50";
  }
  if (serverProgress.value >= minProgress) {
    return "border-emerald-500 bg-white";
  }
  return "border-slate-200 bg-white";
};

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
    submit(); // El envío final a Django
  }
};

const maxDate = computed(() => new Date().toISOString().split("T")[0]);
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
              :class="getStatusClass(step.minProgress)"
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

    <div v-else class="w-full max-w-lg">
      <!-- Barra de progreso -->
      <div class="mb-8">
        <div class="flex justify-between text-sm text-slate-500 mb-2">
          <span class="font-bold"
            >Paso {{ pasoActual }} de {{ totalPasos }}</span
          >
        </div>
        <div class="w-full bg-slate-200 rounded-full h2">
          <div class="w-full bg-slate-200 rounded-full h-2">
            <div
              class="bg-emerald-500 h-2 rounded-full transition-all duration-500"
              :style="{ width: `${(pasoActual / totalPasos) * 100}%` }"
            ></div>
          </div>
        </div>
      </div>

      <!-- Formulario -->

      <UCard class="shadox-xl rounded-3xl" :ui="{ body: 'p-8' }">
        <!-- Paso 1 -->
        <form @submit.prevent="handleFormAction">
          <div v-if="pasoActual === 1">
            <h2 class="text-2xl font-bold text-slate-900 mb-1">
              Datos personales
            </h2>
            <p class="text-slate-500 mb-6">Cuéntanos un poco sobre ti</p>

            <div class="flex flex-col gap-4">
              <UFormField label="Nombre" required :error="errors.nombre">
                <UInput
                  v-model="form.nombre"
                  @input="clearError('nombre')"
                  placeholder="Tu nombre"
                  class="w-full"
                />
              </UFormField>

              <UFormField label="Apellidos" required :error="errors.apellidos">
                <UInput
                  v-model="form.apellidos"
                  @input="clearError('apellidos')"
                  placeholder="Tus apellidos"
                  class="w-full"
                />
              </UFormField>
              <UFormField
                label="Fecha de nacimiento"
                required
                :error="errors.fecha_nacimiento"
              >
                <UInput
                  v-model="form.fecha_nacimiento"
                  @input="clearError('fecha_nacimiento')"
                  type="date"
                  :min="'1900-01-01'"
                  :max="maxDate"
                  placeholder="Tu fecha de nacimiento"
                  class="w-full"
                />
              </UFormField>
              <UFormField
                label="Provincia"
                name="ciudad"
                :error="errors.ciudad"
              >
                <UInputMenu
                  :ui="{ base: 'text-gray-900' }"
                  :model-value="CIUDADES.find((c) => c.value === form.ciudad)"
                  :items="CIUDADES"
                  block
                  @update:model-value="(val) => (form.ciudad = val.value)"
                  class="w-full"
                >
                  <template #leading>
                    <UIcon name="i-heroicons-map-pin" class="w-4 h-4" />
                  </template>
                </UInputMenu>
              </UFormField>
            </div>
          </div>
          <div v-else-if="pasoActual === 2">
            <h2 class="text-2xl font-bold text-slate-900 mb-1">
              Tu perfil alérgico
            </h2>
            <p class="text-slate-500 mb-6">¿Qué alergias tienes?</p>

            <div class="flex flex-col gap-4">
              <UFormField
                label="Alergias conocidas"
                required
                :error="errors.alergias"
              >
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
                    @click="toggleAlergia(alergia)"
                  >
                    {{ alergia }}
                  </button>
                </div>
              </UFormField>

              <Transition name="fade-down">
                <div
                  v-if="form.alergias.length > 0"
                  class="flex flex-col gap-3 tr"
                >
                  <p class="text-sm font-semibold text-slate-700">
                    Severidad por alergia
                  </p>
                  <TransitionGroup
                    name="alergia"
                    tag="div"
                    class="flex flex-col gap-3"
                  >
                    <div
                      v-for="alergia in form.alergias"
                      :key="alergia.nombre"
                      class="flex flex-col sm:flex-row sm:items-center gap-3 p-4 bg-slate-50 rounded-2xl border border-slate-200"
                    >
                      <span
                        class="text-sm font-semibold text-slate-800 w-36 shrink-0"
                        >{{ alergia.nombre }}
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
                          @click="setSeveridad(alergia.nombre, severidad.value)"
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

          <div v-else-if="pasoActual === 3">
            <h2 class="text-2xl font-bold text-slate-900 mb-1">Tu cuenta</h2>
            <p class="text-slate-500 mb-6">Último paso, ¡completa tus datos!</p>

            <UFormField
              label="Correo electrónico"
              required
              :error="errors.email"
            >
              <UInput
                v-model="form.email"
                @input="clearError('email')"
                placeholder="email@dominio.com"
                class="w-full"
              />
            </UFormField>

            <UFormField label="Teléfono" :error="errors.telefono">
              <UInput
                v-model="form.telefono"
                :maxlength="15"
                @input="clearError('telefono')"
                @update:model-value="onPhoneInput"
                placeholder="+34 xxx xxx xxx"
                class="w-full"
              />
            </UFormField>

            <UFormField label="Contraseña" required :error="errors.password">
              <UInput
                v-model="form.password"
                @input="clearError('password')"
                :type="showPassword ? 'text' : 'password'"
                placeholder="Tu contraseña"
                class="w-full"
              >
                <template #trailing>
                  <UButton
                    variant="ghost"
                    color="neutral"
                    @click="showPassword = !showPassword"
                  >
                    <UIcon
                      :name="
                        showPassword
                          ? 'material-symbols:visibility-off'
                          : 'material-symbols:visibility'
                      "
                    />
                  </UButton>
                </template>
              </UInput>
            </UFormField>

            <UFormField
              label="Confirmar contraseña"
              required
              :error="errors.password_confirmation"
            >
              <UInput
                v-model="form.password_confirmation"
                :type="showConfirmPassword ? 'text' : 'password'"
                placeholder="Confirma tu contraseña"
                class="w-full"
              >
                <template #trailing>
                  <UButton
                    variant="ghost"
                    color="neutral"
                    @click="showConfirmPassword = !showConfirmPassword"
                  >
                    <UIcon
                      :name="
                        showConfirmPassword
                          ? 'material-symbols:visibility-off'
                          : 'material-symbols:visibility'
                      "
                    />
                  </UButton>
                </template>
              </UInput>
            </UFormField>

            <UFormField
              label="¿Quieres recibir notificaciones?"
              :error="errors.acepta_notificaciones"
            >
              <div class="flex items-center gap-3 mt-1">
                <USwitch v-model="form.acepta_notificaciones" color="success">
                  <span class="text-sm text-slate-500">
                    {{
                      form.acepta_notificaciones
                        ? "Sí, quiero recibir alertas de polen"
                        : "No, gracias"
                    }}
                  </span>
                </USwitch>
              </div>
            </UFormField>

            <UFormField
              label="¿Cómo nos conociste?"
              :error="errors.como_nos_conocio"
              required
            >
              <USelect
                v-model="form.como_nos_conocio"
                :items="[
                  { label: 'Instagram', value: 'instagram' },
                  { label: 'TikTok', value: 'tiktok' },
                  { label: 'Amigos / Otros', value: 'amigos_otros' },
                ]"
                @update:model-value="clearError('como_nos_conocio')"
                placeholder="Selecciona una opción"
                class="w-full"
              />
            </UFormField>
          </div>

          <!-- Botones de navegación -->
          <div class="flex justify-between mt-8">
            <UButton
              v-if="pasoActual > 1"
              type="button"
              color="neutral"
              variant="ghost"
              @click="pasoAnterior"
            >
              <UIcon
                name="material-symbols:arrow-back-ios"
                width="24"
                height="24"
              />
              <span>Atrás</span>
            </UButton>

            <div v-else />

            <UButton
              type="submit"
              color="success"
              :loading="isSubmitting"
              :disabled="isSubmitting"
            >
              <span>{{
                pasoActual < totalPasos
                  ? "Siguiente"
                  : isSubmitting
                    ? "Registrando..."
                    : "Registrarme"
              }}</span>
              <UIcon
                name="material-symbols:arrow-forward-ios"
                width="24"
                height="24"
              />
            </UButton>
          </div>
        </form>
      </UCard>
    </div>
  </div>
</template>

<style>
.alergia-enter-active {
  transition: all 0.5s ease-out;
}
.alergia-leave-active {
  transition: all 0.5s ease-in;
}
.alergia-enter-from,
.alergia-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

.fade-down-enter-active {
  transition: all 0.5s ease-out;
}
.fade-down-leave-active {
  transition: all 0.5s ease-in;
}
.fade-down-enter-from,
.fade-down-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
</style>
