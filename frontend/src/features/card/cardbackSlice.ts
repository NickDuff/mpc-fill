/**
 * State management for cardbacks retrieved from the backend.
 */

import { createSlice } from "@reduxjs/toolkit";

import { APIGetCardbacks } from "@/app/api";
import { AppDispatch, RootState } from "@/app/store";
import { CardbacksState, createAppAsyncThunk } from "@/common/types";
import { selectBackendURL } from "@/features/backend/backendSlice";
import { selectSearchSettings } from "@/features/searchSettings/searchSettingsSlice";
import { setError } from "@/features/toasts/toastsSlice";

//# region async thunk

const typePrefix = "cardbacks/fetchCardbacks";

const fetchCardbacks = createAppAsyncThunk(
  typePrefix,
  async (arg, { getState }) => {
    const state = getState();
    const backendURL = selectBackendURL(state);
    const searchSettings = selectSearchSettings(state);
    return backendURL != null
      ? APIGetCardbacks(backendURL, searchSettings)
      : null;
  }
);

export async function fetchCardbacksAndReportError(dispatch: AppDispatch) {
  try {
    await dispatch(fetchCardbacks()).unwrap();
  } catch (error: any) {
    dispatch(
      setError([typePrefix, { name: error.name, message: error.message }])
    );
    return null;
  }
}

//# endregion

//# region slice configuration

const initialState: CardbacksState = {
  cardbacks: [],
  status: "idle",
  error: null,
};

export const cardbackSlice = createSlice({
  name: "cardbacks",
  initialState,
  reducers: {
    addCardbackDocuments: (state, action) => {
      state.cardbacks = [...action.payload];
    },
  },
  extraReducers(builder) {
    builder
      .addCase(fetchCardbacks.pending, (state, action) => {
        state.status = "loading";
      })
      .addCase(fetchCardbacks.fulfilled, (state, action) => {
        if (action.payload != null) {
          state.status = "succeeded";
          state.cardbacks = [...action.payload];
        } else {
          state.status = "failed";
        }
      })
      .addCase(fetchCardbacks.rejected, (state, action) => {
        state.status = "failed";
        state.error = {
          name: action.error.name ?? null,
          message: action.error.message ?? null,
        };
      });
  },
});

export default cardbackSlice.reducer;

//# endregion

//# region selectors

const defaultEmptyCardbacks: Array<string> = [];
export const selectCardbacks = (state: RootState) =>
  state.cardbacks.cardbacks ?? defaultEmptyCardbacks;

//# endregion
