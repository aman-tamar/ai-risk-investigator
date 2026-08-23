import api from "./axios";
import type {
  InvestigationResult,
  InvestigationHistory,
} from "@/types/investigation";


export const runInvestigation = async (
  transactionId: string
): Promise<InvestigationResult> => {

  const response = await api.get(
    `/api/investigate/${transactionId}`
  );


  return response.data.data;

};



export const getInvestigations = async (): Promise<
  InvestigationHistory[]
> => {

  const response = await api.get<InvestigationHistory[]>(
    "/api/investigations"
  );

  return response.data;
};



export const getInvestigationById = async (
  transactionId: string
): Promise<InvestigationResult> => {

  const response = await api.get<InvestigationResult>(
    `/api/investigations/${transactionId}`
  );

  return response.data;
};