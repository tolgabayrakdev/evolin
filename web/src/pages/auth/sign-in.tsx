import { Container, Title, TextInput, PasswordInput, Button, Stack, Anchor, Text } from "@mantine/core";
import { useForm } from "@mantine/form";
import { Link } from "react-router";

interface SignInFormValues {
  email: string;
  password: string;
}

export default function SignIn() {
  const form = useForm<SignInFormValues>({
    initialValues: {
      email: "",
      password: "",
    },
    validate: {
      email: (value) => (/^\S+@\S+$/.test(value) ? null : "Invalid email"),
      password: (value) => (value.length < 6 ? "Password must be at least 6 characters" : null),
    },
  });

  const handleSubmit = (values: SignInFormValues) => {
    console.log(values);
    // TODO: Implement sign in logic
  };

  return (
    <Container size={420} style={{ marginTop: 80 }}>
      <Title ta="center" mb="xl">
        Sign In
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

          <Anchor component={Link} to="/forgot-password" size="sm" ta="right">
            Forgot password
          </Anchor>

          <Button type="submit" fullWidth mt="md">
            Sign In
          </Button>

          <Text ta="center" mt="md">
            Don't have an account?{" "}
            <Anchor component={Link} to="/sign-up">
              Sign Up
            </Anchor>
          </Text>
        </Stack>
      </form>
    </Container>
  );
}
