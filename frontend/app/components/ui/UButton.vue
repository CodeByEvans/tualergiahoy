<script setup lang="ts">
const props = defineProps<{
  label: string;
  to: string;
}>();
</script>

<template>
  <UButton v-bind="props" :to="props.to" size="xl" class="rounded-full px-10">
    {{ props.label }}
  </UButton>
</template>
