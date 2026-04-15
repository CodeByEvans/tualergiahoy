<script setup lang="ts">
import type { FieldConfig } from "~/types/Forms";
import FormField from "../molecules/FormField.vue";

interface Props {
  fields: FieldConfig[];
  form: any;
  errors: any;
  clearError: (field: string) => void;
  title: string;
  description: string;
}

const props = defineProps<Props>();
</script>

<template>
  <div class="space-y-4">
    <h2 class="text-2xl font-bold text-slate-900 mb-1">{{ title }}</h2>
    <p class="text-slate-500 mb-6">{{ description }}</p>
    <FormField
      v-for="field in fields"
      :key="field.name"
      v-bind="field"
      :max="field.max"
      v-model="form[field.name]"
      :error="errors[field.name]"
      @input="clearError(field.name)"
    />
  </div>
</template>
