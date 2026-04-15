<script setup lang="ts"></script>

<template>
  <section
    class="relative h-svh w-full overflow-hidden flex items-center justify-center"
  >
    <video
      autoplay
      muted
      loop
      playsinline
      class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 min-w-full min-h-full w-auto h-auto object-cover z-0"
    >
      <source src="~/assets/video/hero.mp4" type="video/mp4" />
    </video>

    <div
      class="absolute inset-0 z-10"
      style="
        background: radial-gradient(
          circle,
          rgba(0, 0, 0, 0.2) 0%,
          rgba(15, 60, 50, 0.7) 100%
        );
      "
    />

    <div class="relative z-20 w-full max-w-4xl px-8 text-center">
      <div class="animate-fade-in-up">
        <span
          class="inline-block px-4 py-1.5 mb-6 rounded-full text-white text-sm uppercase tracking-widest border border-white/20 bg-white/15 backdrop-blur-sm"
        >
          Nuevo: Informe personalizado
        </span>

        <h1
          class="text-[clamp(2.5rem,8vw,4.5rem)] leading-[1.1] font-extrabold text-white mb-6"
          style="text-shadow: 0 4px 12px rgba(0, 0, 0, 0.3)"
        >
          Conoce el aire <br />
          que respiras
        </h1>

        <p
          class="text-[clamp(1.1rem,2.5vw,1.3rem)] leading-relaxed text-white/90 max-w-2xl mx-auto mb-10"
        >
          Optimiza tu bienestar con informes personalizados de salud alérgica
          basados en tu ubicación actual.
        </p>

        <div class="flex gap-4 justify-center flex-wrap">
          <NuxtLink
            to="/registro"
            class="bg-emerald-600 text-white px-11 py-4 rounded-xl text-lg font-semibold no-underline shadow-[0_10px_20px_rgba(25,143,94,0.3)] transition-all duration-300 hover:-translate-y-1 hover:shadow-[0_15px_30px_rgba(25,143,94,0.4)] hover:bg-[#1cb678]"
          >
            Empieza gratis
          </NuxtLink>

          <NuxtLink
            to="/info"
            class="bg-white/10 text-white px-11 py-4 rounded-xl text-lg font-semibold no-underline backdrop-blur-sm border border-white/30 transition-all duration-300 hover:bg-white/20"
          >
            Saber más
          </NuxtLink>
        </div>
      </div>
    </div>
  </section>
</template>
