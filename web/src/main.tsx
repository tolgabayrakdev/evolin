import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { MantineProvider } from "@mantine/core";
import { Notifications } from "@mantine/notifications";
import { RouterProvider } from "react-router";
import { router } from "./router";
import "./index.css";
import "@mantine/core/styles.css";
import "@mantine/notifications/styles.css";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <MantineProvider>
      <Notifications position="top-center" />
      <RouterProvider router={router} />
    </MantineProvider>
  </StrictMode>,
);
