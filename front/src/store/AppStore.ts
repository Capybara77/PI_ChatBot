import { makeAutoObservable, runInAction } from 'mobx';

import axios from 'axios';

type Tresponse = {
  reponse: string;
  messages: {
    role: string;
    content: string;
  }[];
};

export class AppStore {
  baseUrl = 'http://84.201.152.12:8899';
  fetchedData: Tresponse | null = null;
  isLoading = false;

  constructor() {
    makeAutoObservable(this);
  }

  getData = async (query: string) => {
    this.isLoading = true;
    try {
      const response = await axios.get(`${this.baseUrl}/chat`, {
        params: {
          input_data: query,
        },
      });

      if (!response || !response.data) return;

      runInAction(() => {
        this.fetchedData = response.data;
      });
    } catch (error) {
      // Handle the error appropriately, e.g., log it or show a user-friendly error message.
      console.error('An error occurred during the HTTP request:', error);
    } finally {
      runInAction(() => {
        this.isLoading = false;
      });
    }
  };

  clearContext = async () => {
    if (!this.fetchedData) return;
    this.isLoading = true;
    await axios.get(`${this.baseUrl}/clear`);
    runInAction(() => {
      this.fetchedData = null;
      this.isLoading = false;
    });
  };
}
