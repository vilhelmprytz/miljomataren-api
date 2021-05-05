import Head from "next/head";
import styles from "../styles/Home.module.css";
import Link from "next/link";
import useUser from "../lib/useUser";
import useTrips from "../lib/useTrips";

export default function Index({ backendUrl }) {
  const { user } = useUser({ backendUrl: backendUrl, redirectTo: "/login" });
  const { trips, loadingTrips } = useTrips(backendUrl, user);

  if (!user || !trips) return <div>loading...</div>;

  if (!user?.code == 200 || loadingTrips) {
    return <p>loading...</p>;
  }

  return (
    <div className={styles.container}>
      <Head>
        <title>Miljömätaren</title>
        <meta name="description" content="Miljömätaren" />
      </Head>

      <main className={styles.main}>
        <h1 className={styles.title}>Miljömätaren</h1>
        <p>Logged in as {user.response.name}</p>

        <div>
          <p>Trips</p>
          {trips.response.forEach((trip) => {
            return (
              <Link href={`/trip/${trip.id}`}>
                <p>#{trip.id}</p>
              </Link>
            );
          })}
        </div>
      </main>
    </div>
  );
}

export async function getServerSideProps(context) {
  return {
    props: { backendUrl: process.env.BACKEND_URL }, // will be passed to the page component as props
  };
}
