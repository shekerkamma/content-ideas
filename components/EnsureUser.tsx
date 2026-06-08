"use client";

import { useUser } from "@clerk/nextjs";
import { useMutation } from "convex/react";
import { useEffect } from "react";
import { api } from "@/convex/_generated/api";

export function EnsureUser() {
  const convexUrl = process.env.NEXT_PUBLIC_CONVEX_URL;

  if (!convexUrl) {
    return null;
  }

  return <EnsureUserWithConvex />;
}

function EnsureUserWithConvex() {
  const { user, isLoaded } = useUser();
  const upsertCurrentUser = useMutation(api.users.upsertCurrentUser);

  useEffect(() => {
    if (!isLoaded || !user) {
      return;
    }

    void upsertCurrentUser({
      clerkId: user.id,
      name: user.fullName ?? user.primaryEmailAddress?.emailAddress ?? "DealForge user",
      email: user.primaryEmailAddress?.emailAddress
    });
  }, [isLoaded, upsertCurrentUser, user]);

  return null;
}
