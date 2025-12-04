import { useState, useEffect } from 'react';
import {
  AppLayout,
  SideNavigation,
  TopNavigation,
  Container,
  Header,
  Table,
  Button,
  SpaceBetween,
  Box,
  StatusIndicator,
  Badge,
  Pagination,
  Select,
  Modal,
  FormField,
  Input,
  DatePicker,
  Textarea,
  Toggle,
} from '@cloudscape-design/components';
import '@cloudscape-design/global-styles/index.css';

const API_BASE_URL = 'https://myto1dwcaa.execute-api.us-west-2.amazonaws.com/prod';

interface Event {
  eventId: string;
  title: string;
  description: string;
  date: string;
  location: string;
  capacity: number;
  organizer: string;
  status: string;
  waitlistEnabled: boolean;
  currentRegistrations: number;
  currentWaitlist: number;
}

interface User {
  userId: string;
  name: string;
  createdAt: string;
  updatedAt: string;
}

interface Registration {
  registrationId: string;
  eventId: string;
  userId: string;
  status: string;
  registeredAt: string;
  position: number | null;
  user?: User;
  event?: Event;
}

function App() {
  const [activeView, setActiveView] = useState('events');
  const [events, setEvents] = useState<Event[]>([]);
  const [users, setUsers] = useState<User[]>([]);
  const [registrations, setRegistrations] = useState<Registration[]>([]);
  const [selectedItems, setSelectedItems] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [statusFilter, setStatusFilter] = useState<{ label: string; value: string } | null>(null);
  
  // Modal states
  const [showCreateEventModal, setShowCreateEventModal] = useState(false);
  const [showCreateUserModal, setShowCreateUserModal] = useState(false);
  
  // Form states
  const [eventForm, setEventForm] = useState({
    eventId: '',
    title: '',
    description: '',
    date: '',
    location: '',
    capacity: '',
    organizer: '',
    status: 'active',
    waitlistEnabled: false,
  });
  
  const [userForm, setUserForm] = useState({
    userId: '',
    name: '',
  });

  // Fetch data
  const fetchEvents = async () => {
    setLoading(true);
    try {
      const url = statusFilter 
        ? `${API_BASE_URL}/events?status=${statusFilter.value}`
        : `${API_BASE_URL}/events`;
      const response = await fetch(url);
      const data = await response.json();
      setEvents(data);
    } catch (error) {
      console.error('Error fetching events:', error);
    }
    setLoading(false);
  };

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/users`);
      const data = await response.json();
      setUsers(data);
    } catch (error) {
      console.error('Error fetching users:', error);
    }
    setLoading(false);
  };

  const fetchRegistrations = async () => {
    setLoading(true);
    try {
      // Fetch all events and their registrations
      const eventsResponse = await fetch(`${API_BASE_URL}/events`);
      const eventsData = await eventsResponse.json();
      
      const allRegistrations: Registration[] = [];
      for (const event of eventsData) {
        const regResponse = await fetch(`${API_BASE_URL}/events/${event.eventId}/registrations`);
        const regData = await regResponse.json();
        allRegistrations.push(...regData.registered, ...regData.waitlisted);
      }
      
      setRegistrations(allRegistrations);
    } catch (error) {
      console.error('Error fetching registrations:', error);
    }
    setLoading(false);
  };

  useEffect(() => {
    if (activeView === 'events') {
      fetchEvents();
    } else if (activeView === 'users') {
      fetchUsers();
    } else if (activeView === 'registrations') {
      fetchRegistrations();
    }
  }, [activeView, statusFilter]);

  // Create event
  const handleCreateEvent = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/events`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...eventForm,
          capacity: parseInt(eventForm.capacity),
        }),
      });
      
      if (response.ok) {
        setShowCreateEventModal(false);
        setEventForm({
          eventId: '',
          title: '',
          description: '',
          date: '',
          location: '',
          capacity: '',
          organizer: '',
          status: 'active',
          waitlistEnabled: false,
        });
        fetchEvents();
      }
    } catch (error) {
      console.error('Error creating event:', error);
    }
  };

  // Create user
  const handleCreateUser = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/users`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userForm),
      });
      
      if (response.ok) {
        setShowCreateUserModal(false);
        setUserForm({ userId: '', name: '' });
        fetchUsers();
      }
    } catch (error) {
      console.error('Error creating user:', error);
    }
  };

  // Delete event
  const handleDeleteEvent = async () => {
    if (selectedItems.length === 0) return;
    
    try {
      for (const item of selectedItems) {
        await fetch(`${API_BASE_URL}/events/${item.eventId}`, {
          method: 'DELETE',
        });
      }
      setSelectedItems([]);
      fetchEvents();
    } catch (error) {
      console.error('Error deleting event:', error);
    }
  };

  // Delete user
  const handleDeleteUser = async () => {
    if (selectedItems.length === 0) return;
    
    try {
      for (const item of selectedItems) {
        await fetch(`${API_BASE_URL}/users/${item.userId}`, {
          method: 'DELETE',
        });
      }
      setSelectedItems([]);
      fetchUsers();
    } catch (error) {
      console.error('Error deleting user:', error);
    }
  };

  // Unregister
  const handleUnregister = async () => {
    if (selectedItems.length === 0) return;
    
    try {
      for (const item of selectedItems) {
        await fetch(`${API_BASE_URL}/events/${item.eventId}/registrations/${item.userId}`, {
          method: 'DELETE',
        });
      }
      setSelectedItems([]);
      fetchRegistrations();
    } catch (error) {
      console.error('Error unregistering:', error);
    }
  };

  return (
    <>
      <TopNavigation
        identity={{
          href: '#',
          title: 'Event Management',
          logo: { src: '', alt: 'Event Management' },
        }}
        utilities={[
          {
            type: 'button',
            iconName: 'notification',
            ariaLabel: 'Notifications',
          },
          {
            type: 'button',
            iconName: 'settings',
            ariaLabel: 'Settings',
          },
        ]}
      />
      
      <AppLayout
        navigation={
          <SideNavigation
            header={{ text: 'Event Management', href: '#' }}
            activeHref={`#${activeView}`}
            onFollow={(event) => {
              event.preventDefault();
              const view = event.detail.href.replace('#', '');
              setActiveView(view);
              setSelectedItems([]);
            }}
            items={[
              { type: 'link', text: 'Events', href: '#events' },
              { type: 'link', text: 'Users', href: '#users' },
              { type: 'link', text: 'Registrations', href: '#registrations' },
            ]}
          />
        }
        content={
          <SpaceBetween size="l">
            <Header
              variant="h1"
              description="Manage events, users, and registrations"
              actions={
                <SpaceBetween direction="horizontal" size="xs">
                  {activeView === 'events' && (
                    <Button variant="primary" iconName="add-plus" onClick={() => setShowCreateEventModal(true)}>
                      Create event
                    </Button>
                  )}
                  {activeView === 'users' && (
                    <Button variant="primary" iconName="add-plus" onClick={() => setShowCreateUserModal(true)}>
                      Create user
                    </Button>
                  )}
                </SpaceBetween>
              }
            >
              Event Management
            </Header>

            {/* Events View */}
            {activeView === 'events' && (
              <Container
                header={
                  <Header
                    variant="h2"
                    counter={`(${events.length})`}
                    description="View and manage all events"
                    actions={
                      <SpaceBetween direction="horizontal" size="xs">
                        <Button iconName="refresh" onClick={fetchEvents}>Refresh</Button>
                        <Select
                          selectedOption={statusFilter}
                          onChange={({ detail }) => setStatusFilter(detail.selectedOption as { label: string; value: string } | null)}
                          options={[
                            { label: 'All statuses', value: '' },
                            { label: 'Active', value: 'active' },
                            { label: 'Completed', value: 'completed' },
                            { label: 'Cancelled', value: 'cancelled' },
                          ]}
                          placeholder="Filter by status"
                          selectedAriaLabel="Selected"
                        />
                      </SpaceBetween>
                    }
                  >
                    Events
                  </Header>
                }
              >
                <Table
                  columnDefinitions={[
                    {
                      id: 'title',
                      header: 'Event name',
                      cell: (item) => <a href="#">{item.title}</a>,
                      sortingField: 'title',
                    },
                    {
                      id: 'status',
                      header: 'Status',
                      cell: (item) => (
                        <StatusIndicator type={
                          item.status === 'active' ? 'success' :
                          item.status === 'completed' ? 'info' : 'stopped'
                        }>
                          {item.status.charAt(0).toUpperCase() + item.status.slice(1)}
                        </StatusIndicator>
                      ),
                    },
                    {
                      id: 'date',
                      header: 'Event date',
                      cell: (item) => item.date,
                      sortingField: 'date',
                    },
                    {
                      id: 'registrations',
                      header: 'Registrations',
                      cell: (item) => `${item.currentRegistrations || 0}/${item.capacity}`,
                    },
                    {
                      id: 'location',
                      header: 'Location',
                      cell: (item) => item.location,
                    },
                    {
                      id: 'organizer',
                      header: 'Organizer',
                      cell: (item) => item.organizer,
                    },
                  ]}
                  items={events}
                  loading={loading}
                  loadingText="Loading events"
                  selectionType="multi"
                  selectedItems={selectedItems}
                  onSelectionChange={({ detail }) => setSelectedItems(detail.selectedItems)}
                  empty={
                    <Box textAlign="center" color="inherit">
                      <b>No events</b>
                      <Box padding={{ bottom: 's' }} variant="p" color="inherit">
                        No events to display.
                      </Box>
                      <Button onClick={() => setShowCreateEventModal(true)}>Create event</Button>
                    </Box>
                  }
                  header={
                    <Header
                      counter={`(${events.length})`}
                      actions={
                        <SpaceBetween direction="horizontal" size="xs">
                          <Button disabled={selectedItems.length === 0} onClick={handleDeleteEvent}>
                            Delete
                          </Button>
                        </SpaceBetween>
                      }
                    >
                      Events ({events.length})
                    </Header>
                  }
                  pagination={<Pagination currentPageIndex={1} pagesCount={10} />}
                />
              </Container>
            )}

            {/* Users View */}
            {activeView === 'users' && (
              <Container
                header={
                  <Header
                    variant="h2"
                    counter={`(${users.length})`}
                    description="View and manage all users"
                    actions={
                      <Button iconName="refresh" onClick={fetchUsers}>Refresh</Button>
                    }
                  >
                    Users
                  </Header>
                }
              >
                <Table
                  columnDefinitions={[
                    {
                      id: 'name',
                      header: 'User name',
                      cell: (item) => <a href="#">{item.name}</a>,
                      sortingField: 'name',
                    },
                    {
                      id: 'userId',
                      header: 'User ID',
                      cell: (item) => item.userId,
                    },
                    {
                      id: 'createdAt',
                      header: 'Created',
                      cell: (item) => new Date(item.createdAt).toLocaleString(),
                      sortingField: 'createdAt',
                    },
                  ]}
                  items={users}
                  loading={loading}
                  loadingText="Loading users"
                  selectionType="multi"
                  selectedItems={selectedItems}
                  onSelectionChange={({ detail }) => setSelectedItems(detail.selectedItems)}
                  empty={
                    <Box textAlign="center" color="inherit">
                      <b>No users</b>
                      <Box padding={{ bottom: 's' }} variant="p" color="inherit">
                        No users to display.
                      </Box>
                      <Button onClick={() => setShowCreateUserModal(true)}>Create user</Button>
                    </Box>
                  }
                  header={
                    <Header
                      counter={`(${users.length})`}
                      actions={
                        <SpaceBetween direction="horizontal" size="xs">
                          <Button disabled={selectedItems.length === 0} onClick={handleDeleteUser}>
                            Delete
                          </Button>
                        </SpaceBetween>
                      }
                    >
                      Users ({users.length})
                    </Header>
                  }
                />
              </Container>
            )}

            {/* Registrations View */}
            {activeView === 'registrations' && (
              <Container
                header={
                  <Header
                    variant="h2"
                    counter={`(${registrations.length})`}
                    description="View and manage event registrations"
                    actions={
                      <Button iconName="refresh" onClick={fetchRegistrations}>Refresh</Button>
                    }
                  >
                    Registrations
                  </Header>
                }
              >
                <Table
                  columnDefinitions={[
                    {
                      id: 'user',
                      header: 'User',
                      cell: (item) => <a href="#">{item.user?.name || item.userId}</a>,
                    },
                    {
                      id: 'event',
                      header: 'Event',
                      cell: (item) => <a href="#">{item.event?.title || item.eventId}</a>,
                    },
                    {
                      id: 'status',
                      header: 'Status',
                      cell: (item) => (
                        <StatusIndicator type={item.status === 'registered' ? 'success' : 'pending'}>
                          {item.status.charAt(0).toUpperCase() + item.status.slice(1)}
                        </StatusIndicator>
                      ),
                    },
                    {
                      id: 'registeredAt',
                      header: 'Registration time',
                      cell: (item) => new Date(item.registeredAt).toLocaleString(),
                    },
                    {
                      id: 'position',
                      header: 'Waitlist position',
                      cell: (item) => item.position ? <Badge color="blue">{item.position}</Badge> : '-',
                    },
                  ]}
                  items={registrations}
                  loading={loading}
                  loadingText="Loading registrations"
                  selectionType="multi"
                  selectedItems={selectedItems}
                  onSelectionChange={({ detail }) => setSelectedItems(detail.selectedItems)}
                  empty={
                    <Box textAlign="center" color="inherit">
                      <b>No registrations</b>
                      <Box padding={{ bottom: 's' }} variant="p" color="inherit">
                        No registrations to display.
                      </Box>
                    </Box>
                  }
                  header={
                    <Header
                      counter={`(${registrations.length})`}
                      actions={
                        <Button disabled={selectedItems.length === 0} onClick={handleUnregister}>
                          Unregister
                        </Button>
                      }
                    >
                      Registrations ({registrations.length})
                    </Header>
                  }
                  pagination={<Pagination currentPageIndex={1} pagesCount={25} />}
                />
              </Container>
            )}
          </SpaceBetween>
        }
        toolsHide
        navigationWidth={200}
      />

      {/* Create Event Modal */}
      <Modal
        visible={showCreateEventModal}
        onDismiss={() => setShowCreateEventModal(false)}
        header="Create event"
        footer={
          <Box float="right">
            <SpaceBetween direction="horizontal" size="xs">
              <Button variant="link" onClick={() => setShowCreateEventModal(false)}>
                Cancel
              </Button>
              <Button variant="primary" onClick={handleCreateEvent}>
                Create
              </Button>
            </SpaceBetween>
          </Box>
        }
      >
        <SpaceBetween size="m">
          <FormField label="Event ID">
            <Input
              value={eventForm.eventId}
              onChange={({ detail }) => setEventForm({ ...eventForm, eventId: detail.value })}
              placeholder="Leave empty for auto-generated ID"
            />
          </FormField>
          <FormField label="Title">
            <Input
              value={eventForm.title}
              onChange={({ detail }) => setEventForm({ ...eventForm, title: detail.value })}
            />
          </FormField>
          <FormField label="Description">
            <Textarea
              value={eventForm.description}
              onChange={({ detail }) => setEventForm({ ...eventForm, description: detail.value })}
            />
          </FormField>
          <FormField label="Date">
            <DatePicker
              value={eventForm.date}
              onChange={({ detail }) => setEventForm({ ...eventForm, date: detail.value })}
              placeholder="YYYY-MM-DD"
            />
          </FormField>
          <FormField label="Location">
            <Input
              value={eventForm.location}
              onChange={({ detail }) => setEventForm({ ...eventForm, location: detail.value })}
            />
          </FormField>
          <FormField label="Capacity">
            <Input
              type="number"
              value={eventForm.capacity}
              onChange={({ detail }) => setEventForm({ ...eventForm, capacity: detail.value })}
            />
          </FormField>
          <FormField label="Organizer">
            <Input
              value={eventForm.organizer}
              onChange={({ detail }) => setEventForm({ ...eventForm, organizer: detail.value })}
            />
          </FormField>
          <FormField label="Status">
            <Select
              selectedOption={{ label: eventForm.status, value: eventForm.status }}
              onChange={({ detail }) => setEventForm({ ...eventForm, status: detail.selectedOption.value || 'active' })}
              options={[
                { label: 'Active', value: 'active' },
                { label: 'Completed', value: 'completed' },
                { label: 'Cancelled', value: 'cancelled' },
              ]}
            />
          </FormField>
          <FormField label="Enable waitlist">
            <Toggle
              checked={eventForm.waitlistEnabled}
              onChange={({ detail }) => setEventForm({ ...eventForm, waitlistEnabled: detail.checked })}
            />
          </FormField>
        </SpaceBetween>
      </Modal>

      {/* Create User Modal */}
      <Modal
        visible={showCreateUserModal}
        onDismiss={() => setShowCreateUserModal(false)}
        header="Create user"
        footer={
          <Box float="right">
            <SpaceBetween direction="horizontal" size="xs">
              <Button variant="link" onClick={() => setShowCreateUserModal(false)}>
                Cancel
              </Button>
              <Button variant="primary" onClick={handleCreateUser}>
                Create
              </Button>
            </SpaceBetween>
          </Box>
        }
      >
        <SpaceBetween size="m">
          <FormField label="User ID">
            <Input
              value={userForm.userId}
              onChange={({ detail }) => setUserForm({ ...userForm, userId: detail.value })}
              placeholder="Leave empty for auto-generated ID"
            />
          </FormField>
          <FormField label="Name">
            <Input
              value={userForm.name}
              onChange={({ detail }) => setUserForm({ ...userForm, name: detail.value })}
            />
          </FormField>
        </SpaceBetween>
      </Modal>
    </>
  );
}

export default App;
