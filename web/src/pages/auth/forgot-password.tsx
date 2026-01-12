import { Container, Title, TextInput, Button, Stack, Anchor, Text } from "@mantine/core";
import { useForm } from "@mantine/form";
import { Link } from "react-router";

interface ForgotPasswordFormValues {
  email: string;
}

export default function ForgotPassword() {
  const form = useForm<ForgotPasswordFormValues>({
    initialValues: {
      email: "",
    },
    validate: {
      email: (value) => (/^\S+@\S+$/.test(value) ? null : "Invalid email"),
    },
  });

  const handleSubmit = (values: ForgotPasswordFormValues) => {
    console.log(values);
    // TODO: Implement forgot password logic
  };

  return (
    <Container size={420} style={{ marginTop: 80 }}>
      <Title ta="center" mb="xl">
        Forgot Password
      </Title>

      <Text ta="center" c="dimmed" size="sm" mb="xl">
        We will send a password reset link to your email address
      </Text>

      <form onSubmit={form.onSubmit(handleSubmit)}>
        <Stack gap="md">
          <TextInput
            label="Email"
            placeholder="example@email.com"
            required
            {...form.getInputProps("email")}
          />

          <Button type="submit" fullWidth mt="md">
            Send Password Reset Link
          </Button>

          <Text ta="center" mt="md">
            <Anchor component={Link} to="/sign-in">
              Back to sign in
            </Anchor>
          </Text>
        </Stack>
      </form>
    </Container>
  );
}
