import { createBrowserRouter } from "react-router";
import Home from "../pages/home";
import NotFound from "../pages/not-found";
import SignIn from "../pages/auth/sign-in";
import SignUp from "../pages/auth/sign-up";
import ForgotPassword from "../pages/auth/forgot-password";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <Home />,
  },
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
    path: "*",
    element: <NotFound />,
  },
]);
