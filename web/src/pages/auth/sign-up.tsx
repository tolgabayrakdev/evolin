import { Container, Title, TextInput, PasswordInput, Button, Stack, Anchor, Text } from "@mantine/core";
import { useForm } from "@mantine/form";
import { Link } from "react-router";

interface SignUpFormValues {
  name: string;
  email: string;
  password: string;
  confirmPassword: string;
}

export default function SignUp() {
  const form = useForm<SignUpFormValues>({
    initialValues: {
      name: "",
      email: "",
      password: "",
      confirmPassword: "",
    },
    validate: {
      name: (value) => (value.length < 2 ? "Name must be at least 2 characters" : null),
      email: (value) => (/^\S+@\S+$/.test(value) ? null : "Invalid email"),
      password: (value) => (value.length < 6 ? "Password must be at least 6 characters" : null),
      confirmPassword: (value, values) =>
        value !== values.password ? "Passwords do not match" : null,
    },
  });

  const handleSubmit = (values: SignUpFormValues) => {
    console.log(values);
    // TODO: Implement sign up logic
  };

  return (
    <Container size={420} style={{ marginTop: 80 }}>
      <Title ta="center" mb="xl">
        Sign Up
      </Title>

      <form onSubmit={form.onSubmit(handleSubmit)}>
        <Stack gap="md">
          <TextInput
            label="Name"
            placeholder="Enter your name"
            required
            {...form.getInputProps("name")}
          />

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

          <Button type="submit" fullWidth mt="md">
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
