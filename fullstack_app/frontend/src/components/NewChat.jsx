const NewChat = ({ contacts, onCreateChat }) => {
    const [selectedUsers, setSelectedUsers] = useState([]);
    const [chatName, setChatName] = useState("");
    const [isGroup, setIsGroup] = useState(false);

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!selectedUsers.length) return;
        onCreateChat({ userIds: selectedUsers, name: chatName, isGroup });
    };

    const toggleUser = (id) => {
        setSelectedUsers((prev) =>
            prev.includes(id) ? prev.filter(u => u !== id) : [...prev, id]
        );
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                placeholder="Chat name (optional)"
                value={chatName}
                onChange={(e) => setChatName(e.target.value)}
            />
            <label>
                <input
                    type="checkbox"
                    checked={isGroup}
                    onChange={() => setIsGroup(!isGroup)}
                />
                Group chat
            </label>
            <ul>
                {contacts.map(c => (
                    <li key={c.id}>
                        <label>
                            <input
                                type="checkbox"
                                checked={selectedUsers.includes(c.id)}
                                onChange={() => toggleUser(c.id)}
                            />
                            {c.username}
                        </label>
                    </li>
                ))}
            </ul>
            <button type="submit">Create Chat</button>
        </form>
    );
};
export default NewChat;