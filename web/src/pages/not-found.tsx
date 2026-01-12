import { Container, Title, Text, Button, Stack } from "@mantine/core";
import { Link } from "react-router";

export default function NotFound() {
  return (
    <Container
      size="md"
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        minHeight: "100vh",
      }}
    >
      <Stack gap="md" align="center">
        <Title order={1} size="4rem" fw={900}>
          404
        </Title>
        <Title order={2}>Page not found!</Title>
        <Text c="dimmed" size="lg" ta="center">
          The page you are looking for does not exist or has been moved.
        </Text>
        <Button component={Link} to="/" mt="md">
          Go to Home
        </Button>
      </Stack>
    </Container>
  );
}
