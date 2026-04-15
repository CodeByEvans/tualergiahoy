<script setup lang="ts">
import type { NavigationMenuItem } from "@nuxt/ui";
import { useIntersectionObserver } from "@vueuse/core";

const activeSection = ref("inicio");

const section = ["inicio", "como-funciona", "beneficios", "faq"];

onMounted(() => {
  section.forEach((id) => {
    const el = document.getElementById(id);
    if (!el) return;

    useIntersectionObserver(
      el,
      ([entry]) => {
        if (entry?.isIntersecting) {
          activeSection.value = id;
        }
      },
      { threshold: 0.5 },
    );
  });
});

const items = computed<NavigationMenuItem[]>(() => [
  {
    label: "Inicio",
    href: "#inicio",
    active: activeSection.value === "inicio",
  },
  {
    label: "Cómo funciona",
    href: "#como-funciona",
    active: activeSection.value === "como-funciona",
  },
  {
    label: "Beneficios",
    href: "#beneficios",
    active: activeSection.value === "beneficios",
  },
  {
    label: "FAQ",
    href: "#faq",
    active: activeSection.value === "faq",
  },
]);
</script>

<template>
  <UHeader>
    <template #title>
      <Logo class="h-14 w-auto" />
    </template>

    <UNavigationMenu :items="items" />

    <template #right> </template>
  </UHeader>
</template>
