import api from "./axios";
import type { Transaction } from "@/types/investigation";


export const getTransactions = async (): Promise<Transaction[]> => {
  const response = await api.get<Transaction[]>("/api/transactions");

  return response.data;
};