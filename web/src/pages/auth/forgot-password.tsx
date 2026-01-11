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
      email: (value) => (/^\S+@\S+$/.test(value) ? null : "Geçersiz email"),
    },
  });

  const handleSubmit = (values: ForgotPasswordFormValues) => {
    console.log(values);
    // TODO: Implement forgot password logic
  };

  return (
    <Container size={420} style={{ marginTop: 80 }}>
      <Title ta="center" mb="xl">
        Şifremi Unuttum
      </Title>

      <Text ta="center" c="dimmed" size="sm" mb="xl">
        Email adresinize şifre sıfırlama linki göndereceğiz
      </Text>

      <form onSubmit={form.onSubmit(handleSubmit)}>
        <Stack gap="md">
          <TextInput
            label="Email"
            placeholder="ornek@email.com"
            required
            {...form.getInputProps("email")}
          />

          <Button type="submit" fullWidth mt="md">
            Şifre Sıfırlama Linki Gönder
          </Button>

          <Text ta="center" mt="md">
            <Anchor component={Link} to="/sign-in">
              Giriş sayfasına dön
            </Anchor>
          </Text>
        </Stack>
      </form>
    </Container>
  );
}
