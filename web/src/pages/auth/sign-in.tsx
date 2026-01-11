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
      email: (value) => (/^\S+@\S+$/.test(value) ? null : "Geçersiz email"),
      password: (value) => (value.length < 6 ? "Şifre en az 6 karakter olmalıdır" : null),
    },
  });

  const handleSubmit = (values: SignInFormValues) => {
    console.log(values);
    // TODO: Implement sign in logic
  };

  return (
    <Container size={420} style={{ marginTop: 80 }}>
      <Title ta="center" mb="xl">
        Giriş Yap
      </Title>

      <form onSubmit={form.onSubmit(handleSubmit)}>
        <Stack gap="md">
          <TextInput
            label="Email"
            placeholder="ornek@email.com"
            required
            {...form.getInputProps("email")}
          />

          <PasswordInput
            label="Şifre"
            placeholder="Şifrenizi girin"
            required
            {...form.getInputProps("password")}
          />

          <Anchor component={Link} to="/forgot-password" size="sm" ta="right">
            Şifremi unuttum
          </Anchor>

          <Button type="submit" fullWidth mt="md">
            Giriş Yap
          </Button>

          <Text ta="center" mt="md">
            Hesabınız yok mu?{" "}
            <Anchor component={Link} to="/sign-up">
              Kayıt Ol
            </Anchor>
          </Text>
        </Stack>
      </form>
    </Container>
  );
}
