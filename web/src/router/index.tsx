import { createBrowserRouter } from "react-router";
import Home from "@/pages/home";
import NotFound from "@/pages/not-found";
import SignIn from "@/pages/auth/sign-in";
import SignUp from "@/pages/auth/sign-up";
import ForgotPassword from "@/pages/auth/forgot-password";
import Settings from "@/pages/settings";
import Accounts from "@/pages/accounts";
import Customers from "@/pages/customers";
import Keys from "@/pages/keys";
import AppLayout from "@/layouts/app-layout";

export const router = createBrowserRouter([
  {
    path: "/sign-in",
    element: <SignIn />,
  },
  {
    path: "/sign-up",
    element: <SignUp />,
  },
  {
    path: "/forgot-password",
    element: <ForgotPassword />,
  },
  {
    element: <AppLayout />,
    children: [
      {
        path: "/",
        element: <Home />,
      },
      {
        path: "/settings",
        element: <Settings />,
      },
      {
        path: "/accounts",
        element: <Accounts />,
      },
      {
        path: "/customers",
        element: <Customers />,
      },
      {
        path: "/keys",
        element: <Keys />,
      },
      {
        path: "*",
        element: <NotFound />,
      },
    ],
  },
]);
