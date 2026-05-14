import type { Page } from "@playwright/test";

export const loginHarxitFlow = async (page: Page) => {
  await page.goto("/");
  await page.getByPlaceholder("Username").fill("harxitflow");
  await page.getByPlaceholder("Password").fill("harxitflow");
  await page.getByRole("button", { name: "Sign In" }).click();
};
