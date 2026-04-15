<script setup lang="ts">
import BeneficiosSection from "~/components/sections/BeneficiosSection.vue";
import ComoFuncionaSection from "~/components/sections/ComoFuncionaSection.vue";
import FAQSection from "~/components/sections/FAQSection.vue";
import HeroSection from "~/components/sections/HeroSection.vue";
</script>

<template>
  <main>
    <HeroSection id="inicio" />
    <ComoFuncionaSection id="como-funciona" />
    <BeneficiosSection id="beneficios" />
    <FAQSection id="faq" />
  </main>
</template>
