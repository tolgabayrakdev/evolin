import { useState } from "react";
import { Container, Title, TextInput, PasswordInput, Button, Stack, Anchor, Text, Paper } from "@mantine/core";
import { useForm } from "@mantine/form";
import { notifications } from "@mantine/notifications";
import { Link } from "react-router";
import { useAuthStore } from "@/store/auth-store";

interface SignUpFormValues {
  email: string;
  password: string;
  confirmPassword: string;
}

export default function SignUp() {
  const { register } = useAuthStore();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);

  const form = useForm<SignUpFormValues>({
    initialValues: {
      email: "",
      password: "",
      confirmPassword: "",
    },
    validate: {
      email: (value) => (/^\S+@\S+$/.test(value) ? null : "Invalid email"),
      password: (value) => (value.length < 8 ? "Password must be at least 8 characters" : null),
      confirmPassword: (value, values) =>
        value !== values.password ? "Passwords do not match" : null,
    },
  });

  const handleSubmit = async (values: SignUpFormValues) => {
    setIsSubmitting(true);

    const result = await register({
      email: values.email,
      password: values.password,
    });

    setIsSubmitting(false);

    if (result.success) {
      setIsSuccess(true);
      notifications.show({
        title: "Success",
        message: "Account created successfully!",
        color: "green",
        withCloseButton: false,
      });
    } else {
      notifications.show({
        title: "Error",
        message: result.error || "Failed to create account",
        color: "red",
        withCloseButton: false,
      });
    }
  };

  if (isSuccess) {
    return (
      <Container size={420} style={{ marginTop: 80 }}>
        <Paper p="xl" radius="md" withBorder>
          <Stack gap="md" align="center">
            <Title ta="center" order={2}>
              Account Created Successfully!
            </Title>
            <Text ta="center" c="dimmed">
              Your account has been created. You can now sign in.
            </Text>
            <Link
              to="/sign-in"
            >
              Sign In
            </Link>
          </Stack>
        </Paper>
      </Container>
    );
  }

  return (
    <Container size={420} style={{ marginTop: 80 }}>
      <Title ta="center" mb="xl">
        Sign Up
      </Title>

      <form onSubmit={form.onSubmit(handleSubmit)}>
        <Stack gap="md">
          <TextInput
            label="Email"
            placeholder="example@email.com"
            required
            {...form.getInputProps("email")}
          />

          <PasswordInput
            label="Password"
            placeholder="Enter your password"
            required
            {...form.getInputProps("password")}
          />

          <PasswordInput
            label="Confirm Password"
            placeholder="Re-enter your password"
            required
            {...form.getInputProps("confirmPassword")}
          />

          <Button type="submit" fullWidth mt="md" loading={isSubmitting}>
            Sign Up
          </Button>

          <Text ta="center" mt="md">
            Already have an account?{" "}
            <Anchor component={Link} to="/sign-in">
              Sign In
            </Anchor>
          </Text>
        </Stack>
      </form>
    </Container>
  );
}
