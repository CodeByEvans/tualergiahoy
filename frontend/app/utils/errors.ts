export class ApiError extends Error {
  data: any;
  status: number;

  constructor(message: string, data: any, status: number) {
    super(message);
    this.name = "ApiError";
    this.data = data;
    this.status = status;
  }
}
