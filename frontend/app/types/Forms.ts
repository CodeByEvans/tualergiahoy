export type FieldType = "input" | "select" | "menu" | "switch" | "phone";

export interface FieldConfig {
  name: string;
  label: string;
  inputType?: FieldType;
  type?: string;
  placeholder?: string;
  required?: boolean;
  items?: any[];
  icon?: string;
  max?: string;
  maxlength?: number;
  isPassword?: boolean;
}
