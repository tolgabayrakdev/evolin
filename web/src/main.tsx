import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { createTheme, MantineProvider } from "@mantine/core";
import { Notifications } from "@mantine/notifications";
import { RouterProvider } from "react-router";
import { router } from "./router";
import "./index.css";
import "@mantine/core/styles.css";
import "@mantine/notifications/styles.css";


const theme = createTheme({
    fontFamily: 'JetBrains Mono, Open Sans, sans-serif',
    primaryColor: 'indigo'
})


createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <MantineProvider theme={theme}>
      <Notifications position="bottom-center" />
      <RouterProvider router={router} />
    </MantineProvider>
  </StrictMode>,
);
