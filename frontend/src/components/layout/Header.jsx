import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";

export default function Header() {
    return (
        <header className="flex items-center justify-between border-b bg-white px-8 py-4">
            <h2 className="text-2xl font-bold">Dashboard</h2>

            <div className="flex items-center gap-4">
                <Badge>100 Credits</Badge>

                <Avatar>
                    <AvatarFallback>YB</AvatarFallback>
                </Avatar>
            </div>
        </header>
    );
}