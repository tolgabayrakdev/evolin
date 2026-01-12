import {
  NavLink,
  Button,
  Stack,
  Divider,
  Drawer,
  ActionIcon,
  Text,
  Group,
} from "@mantine/core";
import { useMediaQuery } from "@mantine/hooks";
import { useNavigate, useLocation } from "react-router";
import { useAuthStore } from "@/store/auth-store";

interface AppSidebarProps {
  opened: boolean;
  toggle: () => void;
}

interface MenuItem {
  label: string;
  icon: string;
  path: string;
}

const menuItems: MenuItem[] = [
  { label: "Home", icon: "🏠", path: "/" },
  { label: "Settings", icon: "⚙️", path: "/settings" },
  { label: "Accounts", icon: "👥", path: "/accounts" },
  { label: "Customers", icon: "🤝", path: "/customers" },
  { label: "Keys", icon: "🔑", path: "/keys" },
];

export default function AppSidebar({ opened, toggle }: AppSidebarProps) {
  const navigate = useNavigate();
  const location = useLocation();
  const { logout } = useAuthStore();
  const isMobile = useMediaQuery("(max-width: 767px)");

  const handleLogout = async () => {
    await logout();
    navigate("/sign-in");
  };

  const handleNavClick = (path: string) => {
    navigate(path);
    // Only close sidebar on mobile (drawer), keep open on desktop
    if (isMobile) {
      toggle();
    }
  };

  const sidebarContent = (
    <Stack gap="md" h="100%" style={{ padding: 0 }}>
      {/* Header */}
      <Group gap="sm" p="md" style={{ borderBottom: "1px solid var(--mantine-color-default-border)" }}>
        <Text fw={600} size="lg">
          Menu
        </Text>
      </Group>

      {/* Menu Items */}
      <Stack gap={4} style={{ flex: 1, padding: "0.5rem" }}>
        {menuItems.map((item) => (
          <NavLink
            key={item.path}
            label={
              <Group gap="sm">
                <Text size="lg">{item.icon}</Text>
                <Text>{item.label}</Text>
              </Group>
            }
            onClick={() => handleNavClick(item.path)}
            active={location.pathname === item.path}
          />
        ))}
      </Stack>

      <Divider />

      {/* Logout Button */}
      <div style={{ padding: "0.5rem" }}>
        <Button
          variant="light"
          color="red"
          fullWidth
          onClick={handleLogout}
        >
          Logout
        </Button>
      </div>
    </Stack>
  );

  return (
    <>
      {/* Mobile Drawer */}
      <Drawer
        opened={opened}
        onClose={toggle}
        title="Menu"
        size="280px"
        hiddenFrom="sm"
        overlayProps={{ backgroundOpacity: 0.55, blur: 3 }}
      >
        {sidebarContent}
      </Drawer>

      {/* Desktop Sidebar */}
      <div
        style={{
          width: "280px",
          height: "100vh",
          position: "fixed",
          left: opened ? "0" : "-280px",
          top: 0,
          backgroundColor: "var(--mantine-color-body)",
          borderRight: "1px solid var(--mantine-color-default-border)",
          zIndex: 100,
          transition: "left 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
          display: "none",
        }}
        className="desktop-sidebar"
      >
        {sidebarContent}
      </div>
    </>
  );
}

export function SidebarToggle({ opened, toggle }: AppSidebarProps) {
  return (
    <ActionIcon
      variant="subtle"
      onClick={toggle}
      size="lg"
      style={{
        position: "fixed",
        top: "1rem",
        left: opened ? "295px" : "1rem",
        zIndex: 200,
        transition: "left 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
      }}
      visibleFrom="sm"
    >
      {opened ? "×" : "☰"}
    </ActionIcon>
  );
}
