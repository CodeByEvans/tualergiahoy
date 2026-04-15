<script setup lang="ts">
export interface FormFieldProps {
  label: string;
  modelValue?: any;
  error?: string;
  inputType?: "input" | "select" | "menu" | "switch" | "phone";
  type?: string;
  placeholder?: string;
  required?: boolean;
  items?: any[];
  icon?: string;
  max?: string;
  min?: string;
}

const isPasswordVisible = ref(false);

const currentInputType = computed(() => {
  if (props.type === "password") {
    return isPasswordVisible.value ? "text" : "password";
  }
  return props.type;
});

const props = withDefaults(defineProps<FormFieldProps>(), {
  inputType: "input",
  type: "text",
  items: () => [],
});

defineEmits(["update:modelValue", "input"]);
</script>

<template>
  <UFormField :label="label" :required="required" :error="error">
    <UInput
      v-if="inputType === 'input'"
      :model-value="modelValue"
      :type="currentInputType"
      :placeholder="placeholder"
      :icon="icon"
      :max="max"
      class="w-full"
      @update:model-value="$emit('update:modelValue', $event)"
      @input="$emit('input')"
    >
      <template v-if="type === 'password'" #trailing>
        <UButton
          color="primary"
          variant="ghost"
          :padded="false"
          @click="isPasswordVisible = !isPasswordVisible"
        >
          <template #default>
            <UIcon
              :name="
                isPasswordVisible
                  ? 'material-symbols:visibility-off-outline'
                  : 'material-symbols:visibility-outline'
              "
              class="w-5 h-5 text-slate-400"
            />
          </template>
        </UButton>
      </template>

      <template v-else-if="$slots.trailing" #trailing>
        <slot name="trailing" />
      </template>
    </UInput>

    <UInputMenu
      v-else-if="inputType === 'menu'"
      :items="items"
      :placeholder="placeholder"
      :ui="{ base: 'text-gray-900' }"
      block
      class="w-full"
      :model-value="items.find((item) => item.value === modelValue)"
      @update:model-value="
        (val) => $emit('update:modelValue', val.value || val)
      "
    >
      <template #leading v-if="icon">
        <UIcon :name="icon" class="w-4 h-4" />
      </template>
    </UInputMenu>

    <div
      v-else-if="inputType === 'switch'"
      class="flex items-center gap-3 mt-1"
    >
      <USwitch
        :model-value="modelValue"
        @update:model-value="$emit('update:modelValue', $event)"
        color="success"
      >
        <span class="text-sm text-slate-500">
          {{
            modelValue ? "Sí, quiero recibir alertas de polen" : "No, gracias"
          }}
        </span>
      </USwitch>
    </div>

    <UInput
      v-else-if="inputType === 'phone'"
      :model-value="modelValue"
      :maxlength="15"
      :placeholder="placeholder"
      class="w-full"
      @update:model-value="
        (val) => {
          const formatted = formatPhoneInput(val);
          $emit('update:modelValue', formatted);
        }
      "
    />

    <USelect
      v-else
      :model-value="modelValue"
      :items="items"
      @update:model-value="$emit('update:modelValue', $event)"
      placeholder="Selecciona una opción"
      class="w-full"
    />
  </UFormField>
</template>
