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
      name: (value) => (value.length < 2 ? "İsim en az 2 karakter olmalıdır" : null),
      email: (value) => (/^\S+@\S+$/.test(value) ? null : "Geçersiz email"),
      password: (value) => (value.length < 6 ? "Şifre en az 6 karakter olmalıdır" : null),
      confirmPassword: (value, values) =>
        value !== values.password ? "Şifreler eşleşmiyor" : null,
    },
  });

  const handleSubmit = (values: SignUpFormValues) => {
    console.log(values);
    // TODO: Implement sign up logic
  };

  return (
    <Container size={420} style={{ marginTop: 80 }}>
      <Title ta="center" mb="xl">
        Kayıt Ol
      </Title>

      <form onSubmit={form.onSubmit(handleSubmit)}>
        <Stack gap="md">
          <TextInput
            label="İsim"
            placeholder="Adınızı girin"
            required
            {...form.getInputProps("name")}
          />

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

          <PasswordInput
            label="Şifre Tekrar"
            placeholder="Şifrenizi tekrar girin"
            required
            {...form.getInputProps("confirmPassword")}
          />

          <Button type="submit" fullWidth mt="md">
            Kayıt Ol
          </Button>

          <Text ta="center" mt="md">
            Zaten hesabınız var mı?{" "}
            <Anchor component={Link} to="/sign-in">
              Giriş Yap
            </Anchor>
          </Text>
        </Stack>
      </form>
    </Container>
  );
}
