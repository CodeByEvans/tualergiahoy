import type { AlergiaNombre, SeveridadValue } from "~/constants/alergias";

export type Alergia = {
  nombre: AlergiaNombre;
  severidad: SeveridadValue;
};
